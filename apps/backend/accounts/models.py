from __future__ import annotations

import uuid

from django.conf import settings
from django.db import models


class Organization(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        SUSPENDED = "suspended", "Suspended"

    class MfaPolicy(models.TextChoices):
        OFF = "off", "Off"
        OPTIONAL = "optional", "Optional"
        REQUIRED = "required", "Required"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(max_length=80, unique=True)
    name = models.CharField(max_length=180)
    status = models.CharField(max_length=24, choices=Status.choices, default=Status.ACTIVE)
    mfa_policy = models.CharField(max_length=24, choices=MfaPolicy.choices, default=MfaPolicy.OFF)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["status"]),
        ]
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class UserProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="relinium_profile", on_delete=models.CASCADE)
    display_name = models.CharField(max_length=180)
    avatar_initials = models.CharField(max_length=8, blank=True)
    locale = models.CharField(max_length=16, default="fr-FR")
    timezone = models.CharField(max_length=64, default="Europe/Paris")
    selected_organization = models.ForeignKey(Organization, null=True, blank=True, related_name="selected_by_profiles", on_delete=models.SET_NULL)
    mfa_required = models.BooleanField(default=False)
    mfa_enrolled = models.BooleanField(default=False)
    last_seen_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["selected_organization"]),
            models.Index(fields=["mfa_required", "mfa_enrolled"]),
        ]
        ordering = ["display_name"]

    def __str__(self) -> str:
        return self.display_name or self.user.get_username()


class OrganizationMembership(models.Model):
    class Role(models.TextChoices):
        OWNER = "owner", "Owner"
        ADMIN = "admin", "Admin"
        ANALYST = "analyst", "Analyst"
        OPERATOR = "operator", "Operator"
        VIEWER = "viewer", "Viewer"

    class Status(models.TextChoices):
        INVITED = "invited", "Invited"
        ACTIVE = "active", "Active"
        SUSPENDED = "suspended", "Suspended"
        REVOKED = "revoked", "Revoked"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(Organization, related_name="memberships", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="organization_memberships", on_delete=models.CASCADE)
    role = models.CharField(max_length=24, choices=Role.choices, default=Role.VIEWER)
    status = models.CharField(max_length=24, choices=Status.choices, default=Status.INVITED)
    invited_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, related_name="sent_membership_invites", on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["organization", "user"], name="uniq_membership_per_org_user")]
        indexes = [
            models.Index(fields=["organization", "role"]),
            models.Index(fields=["organization", "status"]),
            models.Index(fields=["user", "status"]),
        ]
        ordering = ["organization__name", "user__email"]

    def __str__(self) -> str:
        return f"{self.user_id} {self.role} in {self.organization_id}"


class OAuthIdentity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="oauth_identities", on_delete=models.CASCADE)
    provider = models.CharField(max_length=80)
    issuer = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    email_claim_hash = models.CharField(max_length=64, blank=True)
    last_login_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["provider", "issuer", "subject"], name="uniq_oauth_identity_provider_issuer_subject")]
        indexes = [
            models.Index(fields=["user", "provider"]),
            models.Index(fields=["email_claim_hash"]),
            models.Index(fields=["last_login_at"]),
        ]
        ordering = ["provider", "issuer"]

    def __str__(self) -> str:
        return f"{self.provider}:{self.subject}"


class AccessRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"
        CANCELLED = "cancelled", "Cancelled"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email_hash = models.CharField(max_length=64)
    email_redacted = models.CharField(max_length=180)
    organization_hint = models.CharField(max_length=180, blank=True)
    requested_role = models.CharField(max_length=24, choices=OrganizationMembership.Role.choices, default=OrganizationMembership.Role.VIEWER)
    status = models.CharField(max_length=24, choices=Status.choices, default=Status.PENDING)
    message_redacted = models.TextField(blank=True)
    requested_at = models.DateTimeField(auto_now_add=True)
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, related_name="reviewed_access_requests", on_delete=models.SET_NULL)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["email_hash"]),
            models.Index(fields=["status", "requested_at"]),
            models.Index(fields=["requested_role"]),
        ]
        ordering = ["-requested_at"]

    def __str__(self) -> str:
        return f"{self.email_redacted} ({self.status})"


class AuthAuditEvent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    actor_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, related_name="auth_audit_events", on_delete=models.SET_NULL)
    organization = models.ForeignKey(Organization, null=True, blank=True, related_name="auth_audit_events", on_delete=models.SET_NULL)
    action = models.CharField(max_length=120)
    target_type = models.CharField(max_length=120)
    target_ref = models.CharField(max_length=255)
    ip_hash = models.CharField(max_length=64, null=True, blank=True)
    user_agent_redacted = models.CharField(max_length=255, blank=True)
    metadata_redacted = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["actor_user", "created_at"]),
            models.Index(fields=["organization", "created_at"]),
            models.Index(fields=["action"]),
            models.Index(fields=["target_type", "target_ref"]),
            models.Index(fields=["created_at"]),
        ]
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.action} {self.target_type}:{self.target_ref}"
