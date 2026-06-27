from __future__ import annotations

import uuid

from django.db import models


class AuditLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    actor = models.CharField(max_length=160, null=True, blank=True)
    action = models.CharField(max_length=160)
    target_type = models.CharField(max_length=120)
    target_ref = models.CharField(max_length=500)
    metadata_redacted = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["actor"]),
            models.Index(fields=["action"]),
            models.Index(fields=["target_type", "target_ref"]),
            models.Index(fields=["created_at"]),
        ]
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.action} on {self.target_type}:{self.target_ref}"
