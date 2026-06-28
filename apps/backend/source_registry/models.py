from __future__ import annotations

import uuid

from django.db import models

from accounts.models import Organization


class DataSource(models.Model):
    class SourceType(models.TextChoices):
        LOCAL_FOLDER = "local_folder", "Local folder"
        NETWORK_SHARE = "network_share", "Network share"
        SERVER = "server", "Server"
        CLOUD_GED = "cloud_ged", "Cloud / GED"
        OTHER = "other", "Other"

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        READY = "ready", "Ready"
        OBSERVED = "observed", "Observed"
        ERROR = "error", "Error"
        DISABLED = "disabled", "Disabled"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(Organization, null=True, blank=True, related_name="data_sources", on_delete=models.SET_NULL)
    label = models.CharField(max_length=220)
    source_type = models.CharField(max_length=32, choices=SourceType.choices)
    status = models.CharField(max_length=32, choices=Status.choices, default=Status.DRAFT)
    locator_ref = models.CharField(max_length=700, blank=True)
    locator_hash = models.CharField(max_length=64, blank=True)
    read_only = models.BooleanField(default=True)
    include_hidden = models.BooleanField(default=True)
    follow_symlinks = models.BooleanField(default=False)
    exclusions = models.JSONField(default=list, blank=True)
    notes_redacted = models.TextField(blank=True)
    last_observed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["organization", "status"]),
            models.Index(fields=["source_type"]),
            models.Index(fields=["status"]),
            models.Index(fields=["locator_hash"]),
            models.Index(fields=["source_type", "status"]),
        ]
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.label} ({self.source_type}, {self.status})"


class DataSourceAuditEvent(models.Model):
    class EventType(models.TextChoices):
        CREATED = "created", "Created"
        UPDATED = "updated", "Updated"
        DISABLED = "disabled", "Disabled"
        MARKED_READY = "marked_ready", "Marked ready"
        OBSERVATION_REQUESTED = "observation_requested", "Observation requested"
        OBSERVATION_COMPLETED = "observation_completed", "Observation completed"
        OBSERVATION_FAILED = "observation_failed", "Observation failed"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    source = models.ForeignKey(DataSource, related_name="audit_events", on_delete=models.CASCADE)
    event_type = models.CharField(max_length=40, choices=EventType.choices)
    actor_label = models.CharField(max_length=160, null=True, blank=True)
    details_redacted = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["source", "created_at"]),
            models.Index(fields=["event_type"]),
            models.Index(fields=["created_at"]),
        ]
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.event_type} for {self.source_id}"
