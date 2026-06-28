from __future__ import annotations

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings

from .models import AccessRequest, AuthAuditEvent, Organization, OrganizationMembership
from .permissions import PERMISSION_SOURCE_CREATE, get_user_permissions, has_permission
from .services import get_auth_status, request_access


class DummyRequest:
    headers = {}
    META = {}


class PermissionTests(TestCase):
    def test_anonymous_has_no_permissions(self):
        self.assertEqual(get_user_permissions(None, None), set())

    def test_owner_has_source_create_permission(self):
        User = get_user_model()
        user = User.objects.create_user(username="owner@example.test")
        org = Organization.objects.create(slug="acme", name="Acme")
        OrganizationMembership.objects.create(user=user, organization=org, role="owner", status="active")
        self.assertTrue(has_permission(user, org, PERMISSION_SOURCE_CREATE))


class AuthServiceTests(TestCase):
    def test_request_access_redacts_email(self):
        access_request = request_access({"email": "alice@example.test", "organization_hint": "Acme", "requested_role": "viewer"})
        self.assertEqual(AccessRequest.objects.count(), 1)
        self.assertEqual(access_request.email_redacted, "al***@example.test")
        self.assertNotIn("alice", access_request.email_redacted)

    @override_settings(RELINIUM_AUTH_MODE="disabled", RELINIUM_DEV_AUTH_ENABLED=False)
    def test_auth_status_anonymous(self):
        status = get_auth_status(DummyRequest())
        self.assertFalse(status["authenticated"])
        self.assertEqual(status["mode"], "disabled")

    @override_settings(
        RELINIUM_AUTH_MODE="dev",
        RELINIUM_DEV_AUTH_ENABLED=True,
        RELINIUM_DEV_USER_EMAIL="dev@example.test",
        RELINIUM_DEV_USER_NAME="Dev Operator",
        RELINIUM_DEFAULT_ORG="Relinium Local",
        RELINIUM_DEV_USER_ROLE="owner",
        RELINIUM_MFA_REQUIRED_DEFAULT=False,
    )
    def test_auth_status_dev_identity(self):
        status = get_auth_status(DummyRequest())
        self.assertTrue(status["authenticated"])
        self.assertEqual(status["mode"], "dev")
        self.assertEqual(status["organization"].slug, "relinium-local")
        self.assertTrue(AuthAuditEvent.objects.filter(action="dev_identity_resolved").exists())
