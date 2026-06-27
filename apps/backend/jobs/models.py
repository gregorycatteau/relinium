from __future__ import annotations

import uuid

from django.db import models


class BackgroundJob(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        RUNNING = "running", "Running"
        SUCCEEDED = "succeeded", "Succeeded"
        FAILED = "failed", "Failed"
        CANCELLED = "cancelled", "Cancelled"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    kind = models.CharField(max_length=120)
    status = models.CharField(max_length=24, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    error_code = models.CharField(max_length=120, null=True, blank=True)
    error_summary = models.TextField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["kind", "status"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["started_at"]),
        ]
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.kind} job {self.status}"
