from __future__ import annotations

from django.core.exceptions import PermissionDenied

from .models import Organization, OrganizationMembership


ROLE_OWNER = "owner"
ROLE_ADMIN = "admin"
ROLE_ANALYST = "analyst"
ROLE_OPERATOR = "operator"
ROLE_VIEWER = "viewer"

PERMISSION_SOURCE_CREATE = "source:create"
PERMISSION_SOURCE_READ = "source:read"
PERMISSION_SOURCE_UPDATE = "source:update"
PERMISSION_SOURCE_DISABLE = "source:disable"
PERMISSION_SCAN_PREPARE = "scan:prepare"
PERMISSION_SCAN_RUN = "scan:run"
PERMISSION_EVENT_READ = "event:read"
PERMISSION_SCAM_CASE_CREATE = "scam_case:create"
PERMISSION_SCAM_CASE_READ = "scam_case:read"
PERMISSION_SCAM_CASE_UPDATE = "scam_case:update"
PERMISSION_REPORT_GENERATE = "report:generate"
PERMISSION_REPORT_REVIEW = "report:review"
PERMISSION_ADMIN_MANAGE_MEMBERS = "admin:manage_members"
PERMISSION_ADMIN_MANAGE_SECURITY = "admin:manage_security"

ALL_PERMISSIONS = {
    PERMISSION_SOURCE_CREATE,
    PERMISSION_SOURCE_READ,
    PERMISSION_SOURCE_UPDATE,
    PERMISSION_SOURCE_DISABLE,
    PERMISSION_SCAN_PREPARE,
    PERMISSION_SCAN_RUN,
    PERMISSION_EVENT_READ,
    PERMISSION_SCAM_CASE_CREATE,
    PERMISSION_SCAM_CASE_READ,
    PERMISSION_SCAM_CASE_UPDATE,
    PERMISSION_REPORT_GENERATE,
    PERMISSION_REPORT_REVIEW,
    PERMISSION_ADMIN_MANAGE_MEMBERS,
    PERMISSION_ADMIN_MANAGE_SECURITY,
}

ROLE_PERMISSIONS: dict[str, set[str]] = {
    ROLE_OWNER: set(ALL_PERMISSIONS),
    ROLE_ADMIN: set(ALL_PERMISSIONS) - {PERMISSION_SCAN_RUN},
    ROLE_ANALYST: {
        PERMISSION_SOURCE_READ,
        PERMISSION_EVENT_READ,
        PERMISSION_SCAM_CASE_CREATE,
        PERMISSION_SCAM_CASE_READ,
        PERMISSION_SCAM_CASE_UPDATE,
        PERMISSION_REPORT_GENERATE,
        PERMISSION_REPORT_REVIEW,
    },
    ROLE_OPERATOR: {
        PERMISSION_SOURCE_CREATE,
        PERMISSION_SOURCE_READ,
        PERMISSION_SOURCE_UPDATE,
        PERMISSION_SCAN_PREPARE,
        PERMISSION_SCAM_CASE_CREATE,
        PERMISSION_SCAM_CASE_READ,
        PERMISSION_SCAM_CASE_UPDATE,
        PERMISSION_REPORT_GENERATE,
    },
    ROLE_VIEWER: {
        PERMISSION_SOURCE_READ,
        PERMISSION_EVENT_READ,
        PERMISSION_SCAM_CASE_READ,
    },
}


def get_user_organization(user) -> Organization | None:
    if not getattr(user, "is_authenticated", False):
        return None
    profile = getattr(user, "relinium_profile", None)
    selected = getattr(profile, "selected_organization", None)
    if selected and OrganizationMembership.objects.filter(user=user, organization=selected, status=OrganizationMembership.Status.ACTIVE).exists():
        return selected
    membership = (
        OrganizationMembership.objects.select_related("organization")
        .filter(user=user, status=OrganizationMembership.Status.ACTIVE, organization__status=Organization.Status.ACTIVE)
        .order_by("organization__name")
        .first()
    )
    return membership.organization if membership else None


def get_user_permissions(user, organization: Organization | None) -> set[str]:
    if not getattr(user, "is_authenticated", False) or organization is None:
        return set()
    if getattr(user, "is_superuser", False):
        # Superuser bypass is reserved for explicit local/admin operations, not for OIDC users.
        return set(ROLE_PERMISSIONS[ROLE_OWNER])
    membership = OrganizationMembership.objects.filter(user=user, organization=organization, status=OrganizationMembership.Status.ACTIVE).first()
    if membership is None:
        return set()
    return set(ROLE_PERMISSIONS.get(membership.role, set()))


def has_permission(user, organization: Organization | None, permission_code: str) -> bool:
    return permission_code in get_user_permissions(user, organization)


def require_permission(user, organization: Organization | None, permission_code: str) -> None:
    if not getattr(user, "is_authenticated", False):
        raise PermissionDenied("Authentification requise.")
    if not has_permission(user, organization, permission_code):
        raise PermissionDenied("Permission insuffisante.")
