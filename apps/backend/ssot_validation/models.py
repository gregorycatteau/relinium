from __future__ import annotations

import uuid

from django.db import models


class ValidationRun(models.Model):
    class Mode(models.TextChoices):
        STRICT = "strict", "Strict"
        BASELINE = "baseline", "Baseline"

    class Status(models.TextChoices):
        PASSED = "passed", "Passed"
        FAILED = "failed", "Failed"
        ERROR = "error", "Error"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mode = models.CharField(max_length=16, choices=Mode.choices)
    status = models.CharField(max_length=16, choices=Status.choices)
    started_at = models.DateTimeField()
    finished_at = models.DateTimeField(null=True, blank=True)
    finding_count = models.PositiveIntegerField(default=0)
    matched_baseline_count = models.PositiveIntegerField(default=0)
    validator_version = models.CharField(max_length=80, null=True, blank=True)
    ssot_snapshot_hash = models.CharField(max_length=64, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["mode", "status"]),
            models.Index(fields=["started_at"]),
            models.Index(fields=["created_at"]),
        ]
        ordering = ["-started_at", "-created_at"]

    def __str__(self) -> str:
        return f"{self.mode} validation {self.status} ({self.finding_count})"


class ValidationFindingRecord(models.Model):
    run = models.ForeignKey(ValidationRun, related_name="findings", on_delete=models.CASCADE)
    code = models.CharField(max_length=120)
    severity = models.CharField(max_length=32)
    event_id = models.CharField(max_length=160, null=True, blank=True)
    stream_path = models.CharField(max_length=500)
    line_number = models.PositiveIntegerField(null=True, blank=True)
    raw_line_sha256 = models.CharField(max_length=64, null=True, blank=True)
    message_redacted = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["run", "code"]),
            models.Index(fields=["event_id"]),
            models.Index(fields=["stream_path", "line_number"]),
            models.Index(fields=["created_at"]),
        ]
        ordering = ["stream_path", "line_number", "code"]

    def __str__(self) -> str:
        location = f"{self.stream_path}:{self.line_number}" if self.line_number else self.stream_path
        return f"{self.code} at {location}"
