from __future__ import annotations

from django.db import models


class EventStreamIndex(models.Model):
    stream_path = models.CharField(max_length=500, unique=True)
    tenant = models.CharField(max_length=160, null=True, blank=True)
    event_count = models.PositiveIntegerField(default=0)
    last_event_id = models.CharField(max_length=160, null=True, blank=True)
    last_seen_at = models.DateTimeField(null=True, blank=True)
    indexed_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["tenant"]),
            models.Index(fields=["last_seen_at"]),
            models.Index(fields=["indexed_at"]),
        ]
        ordering = ["stream_path"]

    def __str__(self) -> str:
        return f"{self.stream_path} ({self.event_count})"


class SsotDocumentIndex(models.Model):
    path = models.CharField(max_length=500, unique=True)
    exists = models.BooleanField(default=False)
    declared_hash = models.CharField(max_length=64, null=True, blank=True)
    actual_hash = models.CharField(max_length=64, null=True, blank=True)
    hash_status = models.CharField(max_length=40)
    referenced_by_event_id = models.CharField(max_length=160, null=True, blank=True)
    stream_path = models.CharField(max_length=500, null=True, blank=True)
    event_line = models.PositiveIntegerField(null=True, blank=True)
    indexed_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["hash_status"]),
            models.Index(fields=["referenced_by_event_id"]),
            models.Index(fields=["stream_path", "event_line"]),
            models.Index(fields=["indexed_at"]),
        ]
        ordering = ["path"]

    def __str__(self) -> str:
        return f"{self.path} [{self.hash_status}]"
