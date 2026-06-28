from __future__ import annotations

from django.core.exceptions import ValidationError
from django.test import TestCase

from .services import locator_display, validate_source_input


class SourceRegistryRedactionTests(TestCase):
    def test_locator_with_userinfo_is_rejected(self):
        with self.assertRaises(ValidationError):
            validate_source_input(
                {
                    "label": "Partage sensible",
                    "source_type": "network_share",
                    "locator_ref": "smb://user:password@nas.example.local/share",
                }
            )

    def test_locator_with_secret_marker_is_rejected(self):
        with self.assertRaises(ValidationError):
            validate_source_input(
                {
                    "label": "Ged",
                    "source_type": "cloud_ged",
                    "locator_ref": "https://ged.example.local/export?api_key=abc",
                }
            )

    def test_locator_display_masks_raw_locator(self):
        self.assertEqual(locator_display("sftp://files.example.local/departements/finance"), "sftp://files.example.local/.../finance")
        self.assertEqual(locator_display("//nas/comptabilite/confidentiel"), "//nas/.../confidentiel")
        self.assertEqual(locator_display("/srv/relinium/sources/finance"), ".../finance")
