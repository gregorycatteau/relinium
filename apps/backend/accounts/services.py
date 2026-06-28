from __future__ import annotations

import hashlib
import re
from typing import Any

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction
from django.utils import timezone
from django.utils.text import slugify

from .models import AccessRequest, AuthAuditEvent, Organization, OrganizationMembership, UserProfile
from .permissions import get_user_organization, get_user_permissions


EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
SECRET_MARKERS = ("password=", "token=", "api_key=", "secret=", "bearer ")


def hash_text(value: str) -> str:
    return hashlib.sha256(value.strip().lower().encode("utf-8")).hexdigest()


def redact_email(value: str) -> str:
    clean = value.strip().lower()
    if "@" not in clean:
        return "[redacted]"
    local, domain = clean.split("@", 1)
    prefix = local[:2] if len(local) > 1 else local[:1]
    return f"{prefix}***@{domain}"


def initials_for_name(name: str, email: str = "") -> str:
    source = name.strip() or email.split("@", 1)[0]
    parts = [part for part in re.split(r"[\s._-]+", source) if part]
    if not parts:
        return "U"
    return "".join(part[0] for part in parts[:2]).upper()[:4]


def _ensure_no_secret(value: Any, field: str) -> None:
    text = str(value or "").lower()
    if any(marker in text for marker in SECRET_MARKERS):
        raise ValidationError({field: "Cette valeur ressemble à un secret. Ne saisissez aucun mot de passe ni token."})


def _request_ip(request) -> str:
    forwarded = request.headers.get("X-Forwarded-For", "")
    if forwarded:
        return forwarded.split(",", 1)[0].strip()
    return request.META.get("REMOTE_ADDR", "")


def audit_auth_event(
    *,
    request=None,
    actor_user=None,
    organization: Organization | None = None,
    action: str,
    target_type: str,
    target_ref: str,
    metadata_redacted: dict[str, Any] | None = None,
) -> AuthAuditEvent:
    ip_hash = hash_text(_request_ip(request)) if request is not None and _request_ip(request) else None
    user_agent = request.headers.get("User-Agent", "")[:255] if request is not None else ""
    return AuthAuditEvent.objects.create(
        actor_user=actor_user if getattr(actor_user, "is_authenticated", False) else None,
        organization=organization,
        action=action,
        target_type=target_type,
        target_ref=str(target_ref)[:255],
        ip_hash=ip_hash,
        user_agent_redacted=user_agent,
        metadata_redacted=metadata_redacted or {},
    )


def ensure_profile(user, *, display_name: str = "", selected_organization: Organization | None = None) -> UserProfile:
    profile, created = UserProfile.objects.get_or_create(
        user=user,
        defaults={
            "display_name": display_name or user.get_full_name() or user.email or user.get_username(),
            "avatar_initials": initials_for_name(display_name or user.get_full_name(), user.email),
            "selected_organization": selected_organization,
            "mfa_required": settings.RELINIUM_MFA_REQUIRED_DEFAULT,
        },
    )
    updates: list[str] = []
    if selected_organization and profile.selected_organization_id is None:
        profile.selected_organization = selected_organization
        updates.append("selected_organization")
    if not profile.avatar_initials:
        profile.avatar_initials = initials_for_name(profile.display_name, user.email)
        updates.append("avatar_initials")
    if created or updates:
        profile.save(update_fields=updates + ["updated_at"] if updates else None)
    return profile


def get_or_create_dev_identity_if_enabled(request):
    if not settings.RELINIUM_DEV_AUTH_ENABLED:
        return None
    if settings.RELINIUM_AUTH_MODE != "dev":
        raise PermissionDenied("Le mode dev auth exige RELINIUM_AUTH_MODE=dev.")
    role = settings.RELINIUM_DEV_USER_ROLE.lower()
    if role not in {choice.value for choice in OrganizationMembership.Role}:
        role = OrganizationMembership.Role.OWNER
    email = settings.RELINIUM_DEV_USER_EMAIL.strip().lower()
    name = settings.RELINIUM_DEV_USER_NAME.strip() or "Relinium Dev"
    org_name = settings.RELINIUM_DEFAULT_ORG.strip() or "Relinium Local"
    org_slug = slugify(org_name)[:80] or "relinium-local"
    User = get_user_model()
    with transaction.atomic():
        org, _ = Organization.objects.get_or_create(slug=org_slug, defaults={"name": org_name})
        user, created = User.objects.get_or_create(username=email, defaults={"email": email, "first_name": name})
        if created:
            user.set_unusable_password()
            user.save(update_fields=["password"])
        elif user.email != email:
            user.email = email
            user.save(update_fields=["email"])
        ensure_profile(user, display_name=name, selected_organization=org)
        OrganizationMembership.objects.update_or_create(
            organization=org,
            user=user,
            defaults={"role": role, "status": OrganizationMembership.Status.ACTIVE},
        )
        audit_auth_event(
            request=request,
            actor_user=user,
            organization=org,
            action="dev_identity_resolved",
            target_type="user",
            target_ref=str(user.id),
            metadata_redacted={"mode": "dev", "created": created},
        )
    return user


def effective_user(request):
    user = getattr(request, "user", None)
    if getattr(user, "is_authenticated", False):
        return user
    return get_or_create_dev_identity_if_enabled(request)


def get_auth_status(request) -> dict[str, Any]:
    user = effective_user(request)
    organization = get_user_organization(user) if user else None
    profile = getattr(user, "relinium_profile", None) if user else None
    return {
        "authenticated": bool(getattr(user, "is_authenticated", False)),
        "mode": "dev" if settings.RELINIUM_DEV_AUTH_ENABLED and settings.RELINIUM_AUTH_MODE == "dev" else settings.RELINIUM_AUTH_MODE,
        "oidc_configured": settings.RELINIUM_AUTH_MODE == "oidc",
        "dev_auth_enabled": settings.RELINIUM_DEV_AUTH_ENABLED,
        "mfa_required": bool(getattr(profile, "mfa_required", False)),
        "mfa_enrolled": bool(getattr(profile, "mfa_enrolled", False)),
        "user": user,
        "organization": organization,
        "permissions": sorted(get_user_permissions(user, organization)) if user else [],
    }


def request_access(input_data: dict[str, Any], *, request=None) -> AccessRequest:
    email = str(input_data.get("email") or "").strip().lower()
    if not EMAIL_RE.match(email):
        raise ValidationError({"email": "Adresse email professionnelle invalide."})
    organization_hint = str(input_data.get("organization_hint") or input_data.get("organizationHint") or "").strip()[:180]
    requested_role = str(input_data.get("requested_role") or input_data.get("requestedRole") or OrganizationMembership.Role.VIEWER).strip()
    if requested_role not in {choice.value for choice in OrganizationMembership.Role}:
        requested_role = OrganizationMembership.Role.VIEWER
    message = str(input_data.get("message_redacted") or input_data.get("messageRedacted") or "").strip()[:2000]
    _ensure_no_secret(organization_hint, "organization_hint")
    _ensure_no_secret(message, "message_redacted")
    access_request = AccessRequest.objects.create(
        email_hash=hash_text(email),
        email_redacted=redact_email(email),
        organization_hint=organization_hint,
        requested_role=requested_role,
        message_redacted=message,
    )
    audit_auth_event(
        request=request,
        action="access_requested",
        target_type="access_request",
        target_ref=str(access_request.id),
        metadata_redacted={"requested_role": requested_role, "organization_hint": organization_hint[:80]},
    )
    return access_request


def update_profile(user, input_data: dict[str, Any]) -> UserProfile:
    if not getattr(user, "is_authenticated", False):
        raise PermissionDenied("Authentification requise.")
    display_name = str(input_data.get("display_name") or input_data.get("displayName") or "").strip()[:180]
    locale = str(input_data.get("locale") or "fr-FR").strip()[:16]
    timezone_name = str(input_data.get("timezone") or "Europe/Paris").strip()[:64]
    _ensure_no_secret(display_name, "display_name")
    profile = ensure_profile(user)
    profile.display_name = display_name or profile.display_name
    profile.avatar_initials = initials_for_name(profile.display_name, user.email)
    profile.locale = locale or "fr-FR"
    profile.timezone = timezone_name or "Europe/Paris"
    profile.last_seen_at = timezone.now()
    profile.save(update_fields=["display_name", "avatar_initials", "locale", "timezone", "last_seen_at", "updated_at"])
    return profile


def select_organization(user, organization_id: str) -> Organization:
    if not getattr(user, "is_authenticated", False):
        raise PermissionDenied("Authentification requise.")
    membership = OrganizationMembership.objects.select_related("organization").filter(
        user=user,
        organization_id=organization_id,
        status=OrganizationMembership.Status.ACTIVE,
        organization__status=Organization.Status.ACTIVE,
    ).first()
    if membership is None:
        raise PermissionDenied("Permission insuffisante.")
    profile = ensure_profile(user, selected_organization=membership.organization)
    profile.selected_organization = membership.organization
    profile.save(update_fields=["selected_organization", "updated_at"])
    return membership.organization
