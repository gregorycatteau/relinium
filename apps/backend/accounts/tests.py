from __future__ import annotations

import json

from django.contrib.auth import get_user_model
from django.test import Client
from django.test import TestCase, override_settings

from scam_trace.models import ScamCase

from . import services
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
        self.assertEqual(status["permissions"], [])
        self.assertEqual(get_user_model().objects.count(), 0)

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


class GraphqlAuthTests(TestCase):
    def graphql(self, query: str, variables: dict | None = None):
        response = Client().post(
            "/graphql",
            data=json.dumps({"query": query, "variables": variables or {}}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        return response.json()

    @override_settings(RELINIUM_AUTH_MODE="disabled", RELINIUM_DEV_AUTH_ENABLED=False)
    def test_create_data_source_without_auth_is_rejected(self):
        payload = self.graphql(
            """
            mutation {
              createDataSource(input: {label: "Source test", sourceType: LOCAL_FOLDER}) { id }
            }
            """
        )
        self.assertIsNone(payload["data"])
        self.assertEqual(payload["errors"][0]["message"], "Authentification requise.")

    @override_settings(
        RELINIUM_AUTH_MODE="dev",
        RELINIUM_DEV_AUTH_ENABLED=True,
        RELINIUM_DEV_USER_EMAIL="dev@relinium.local",
        RELINIUM_DEV_USER_NAME="Operateur Relinium",
        RELINIUM_DEFAULT_ORG="relinium-local",
        RELINIUM_DEV_USER_ROLE="owner",
        RELINIUM_MFA_REQUIRED_DEFAULT=False,
    )
    def test_create_data_source_with_dev_auth_assigns_org_and_audits(self):
        payload = self.graphql(
            """
            mutation {
              createDataSource(input: {label: "Source test", sourceType: LOCAL_FOLDER}) {
                id
                label
              }
            }
            """
        )
        self.assertNotIn("errors", payload)
        source_id = payload["data"]["createDataSource"]["id"]
        org = Organization.objects.get(slug="relinium-local")
        self.assertTrue(org.data_sources.filter(id=source_id).exists())
        audit = AuthAuditEvent.objects.get(action="source_created", target_ref=source_id)
        metadata = json.dumps(audit.metadata_redacted).lower()
        self.assertNotIn("token", metadata)
        self.assertNotIn("password", metadata)
        self.assertNotIn("api_key", metadata)
        self.assertNotIn("secret", metadata)

    def test_generate_scam_reports_without_permission_is_rejected(self):
        User = get_user_model()
        user = User.objects.create_user(username="viewer@example.test", email="viewer@example.test")
        org = Organization.objects.create(slug="viewer-org", name="Viewer Org")
        services.ensure_profile(user, display_name="Viewer", selected_organization=org)
        OrganizationMembership.objects.create(user=user, organization=org, role="viewer", status="active")
        case = ScamCase.objects.create(organization=org, title="Case", status="active")
        client = Client()
        client.force_login(user)
        response = client.post(
            "/graphql",
            data=json.dumps({"query": f'mutation {{ generateScamReports(caseId: "{case.id}") {{ id }} }}'}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertIsNone(payload["data"])
        self.assertEqual(payload["errors"][0]["message"], "Permission insuffisante.")
