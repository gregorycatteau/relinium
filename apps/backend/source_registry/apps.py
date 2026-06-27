from __future__ import annotations

from django.apps import AppConfig


class SourceRegistryConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "source_registry"
    verbose_name = "Source registry"
