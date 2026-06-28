from __future__ import annotations

import uuid

from django.db import models

from accounts.models import Organization


class ScamCase(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        ACTIVE = "active", "Active"
        READY_FOR_REVIEW = "ready_for_review", "Ready for review"
        REPORTED = "reported", "Reported"
        CLOSED = "closed", "Closed"

    class Severity(models.TextChoices):
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"
        CRITICAL = "critical", "Critical"

    class InitialVector(models.TextChoices):
        EMAIL = "email", "Email"
        SMS = "sms", "SMS"
        CALL = "call", "Call"
        CHAT = "chat", "Messaging"
        DOCUMENT = "document", "Document"
        USB = "usb", "USB"
        WEBSITE = "website", "Website"
        BANK_TRANSACTION = "bank_transaction", "Bank transaction"
        REMOTE_ACCESS = "remote_access", "Remote access"
        OTHER = "other", "Other"

    class VictimType(models.TextChoices):
        INDIVIDUAL = "individual", "Individual"
        COMPANY = "company", "Company"
        ASSOCIATION = "association", "Association"
        PUBLIC_ENTITY = "public_entity", "Public entity"
        UNKNOWN = "unknown", "Unknown"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(Organization, null=True, blank=True, related_name="scam_cases", on_delete=models.SET_NULL)
    title = models.CharField(max_length=220)
    status = models.CharField(max_length=32, choices=Status.choices, default=Status.DRAFT)
    severity = models.CharField(max_length=16, choices=Severity.choices, default=Severity.MEDIUM)
    initial_vector = models.CharField(max_length=32, choices=InitialVector.choices, default=InitialVector.OTHER)
    victim_type = models.CharField(max_length=32, choices=VictimType.choices, default=VictimType.UNKNOWN)
    victim_label_redacted = models.CharField(max_length=220, blank=True)
    discovered_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    summary = models.TextField(blank=True)
    operator_notes_redacted = models.TextField(blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["organization", "status"]),
            models.Index(fields=["status", "severity"]),
            models.Index(fields=["initial_vector"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["updated_at"]),
        ]
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.title} ({self.status})"


class EvidenceArtifact(models.Model):
    class ArtifactType(models.TextChoices):
        EML = "eml", "EML"
        SMS_TEXT = "sms_text", "SMS text"
        SCREENSHOT = "screenshot", "Screenshot"
        CALL_NOTE = "call_note", "Call note"
        DOCUMENT = "document", "Document"
        URL = "url", "URL"
        BANK_RECORD = "bank_record", "Bank record"
        LOG_EXPORT = "log_export", "Log export"
        OTHER = "other", "Other"

    class IntegrityStatus(models.TextChoices):
        DECLARED = "declared", "Declared"
        HASHED = "hashed", "Hashed"
        HASH_MISMATCH = "hash_mismatch", "Hash mismatch"
        UNCHECKED = "unchecked", "Unchecked"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    case = models.ForeignKey(ScamCase, related_name="artifacts", on_delete=models.CASCADE)
    artifact_type = models.CharField(max_length=32, choices=ArtifactType.choices)
    original_filename_redacted = models.CharField(max_length=260, null=True, blank=True)
    sha256 = models.CharField(max_length=64, db_index=True)
    size_bytes = models.PositiveBigIntegerField(null=True, blank=True)
    storage_ref = models.CharField(max_length=500, null=True, blank=True)
    ingested_at = models.DateTimeField(auto_now_add=True)
    source_description = models.TextField(blank=True)
    integrity_status = models.CharField(max_length=32, choices=IntegrityStatus.choices, default=IntegrityStatus.HASHED)
    metadata_redacted = models.JSONField(default=dict, blank=True)
    raw_content_storage_allowed = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=["case", "ingested_at"]),
            models.Index(fields=["sha256"]),
            models.Index(fields=["artifact_type"]),
        ]
        ordering = ["-ingested_at"]

    def __str__(self) -> str:
        return f"{self.artifact_type} {self.sha256[:12]} for {self.case_id}"


class ScamQuestionnaireAnswer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    case = models.ForeignKey(ScamCase, related_name="questionnaire_answers", on_delete=models.CASCADE)
    question_key = models.CharField(max_length=120)
    answer_type = models.CharField(max_length=32)
    answer_value_redacted = models.JSONField(default=dict, blank=True)
    answered_at = models.DateTimeField(auto_now=True)
    confidence = models.FloatField(default=0.7)
    notes_redacted = models.TextField(blank=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["case", "question_key"], name="uniq_scam_answer_per_case_question")]
        indexes = [
            models.Index(fields=["case", "question_key"]),
            models.Index(fields=["answered_at"]),
        ]
        ordering = ["question_key"]

    def __str__(self) -> str:
        return f"{self.question_key} for {self.case_id}"


class TechnicalIndicator(models.Model):
    class IndicatorType(models.TextChoices):
        EMAIL = "email", "Email"
        DOMAIN = "domain", "Domain"
        URL = "url", "URL"
        IP = "ip", "IP"
        PHONE = "phone", "Phone"
        IBAN = "iban", "IBAN"
        CRYPTO_WALLET = "crypto_wallet", "Crypto wallet"
        HASH = "hash", "Hash"
        ATTACHMENT_NAME = "attachment_name", "Attachment name"
        USER_ACCOUNT = "user_account", "User account"
        OTHER = "other", "Other"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    case = models.ForeignKey(ScamCase, related_name="indicators", on_delete=models.CASCADE)
    indicator_type = models.CharField(max_length=32, choices=IndicatorType.choices)
    value_redacted = models.CharField(max_length=500)
    value_hash = models.CharField(max_length=64)
    first_seen_at = models.DateTimeField(auto_now_add=True)
    source_artifact = models.ForeignKey(EvidenceArtifact, null=True, blank=True, related_name="indicators", on_delete=models.SET_NULL)
    risk_level = models.CharField(max_length=16, default="medium")
    confidence = models.FloatField(default=0.7)
    notes_redacted = models.TextField(blank=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["case", "indicator_type", "value_hash"], name="uniq_scam_indicator_per_case")]
        indexes = [
            models.Index(fields=["case", "indicator_type"]),
            models.Index(fields=["indicator_type"]),
            models.Index(fields=["value_hash"]),
            models.Index(fields=["first_seen_at"]),
        ]
        ordering = ["indicator_type", "value_redacted"]

    def __str__(self) -> str:
        return f"{self.indicator_type}:{self.value_redacted}"


class TimelineEvent(models.Model):
    class EventType(models.TextChoices):
        RECEIVED = "received", "Received"
        OPENED = "opened", "Opened"
        CLICKED = "clicked", "Clicked"
        SUBMITTED_CREDENTIALS = "submitted_credentials", "Submitted credentials"
        SUBMITTED_PAYMENT = "submitted_payment", "Submitted payment"
        PHONE_CALL = "phone_call", "Phone call"
        REMOTE_ACCESS = "remote_access", "Remote access"
        TRANSFER = "transfer", "Transfer"
        DISCOVERY = "discovery", "Discovery"
        REMEDIATION = "remediation", "Remediation"
        REPORT = "report", "Report"
        OTHER = "other", "Other"

    class Source(models.TextChoices):
        VICTIM_STATEMENT = "victim_statement", "Victim statement"
        ARTIFACT = "artifact", "Artifact"
        TECHNICAL_ANALYSIS = "technical_analysis", "Technical analysis"
        BANK_RECORD = "bank_record", "Bank record"
        OPERATOR = "operator", "Operator"
        CORRELATION = "correlation", "Correlation"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    case = models.ForeignKey(ScamCase, related_name="timeline_events", on_delete=models.CASCADE)
    occurred_at = models.DateTimeField(null=True, blank=True)
    event_type = models.CharField(max_length=32, choices=EventType.choices)
    label = models.CharField(max_length=220)
    description_redacted = models.TextField(blank=True)
    source = models.CharField(max_length=32, choices=Source.choices)
    confidence = models.FloatField(default=0.7)
    related_artifact = models.ForeignKey(EvidenceArtifact, null=True, blank=True, related_name="timeline_events", on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["case", "occurred_at"]),
            models.Index(fields=["case", "created_at"]),
            models.Index(fields=["event_type"]),
            models.Index(fields=["created_at"]),
        ]
        ordering = ["occurred_at", "created_at"]

    def __str__(self) -> str:
        return f"{self.label} ({self.event_type})"


class CustodyEvent(models.Model):
    class Action(models.TextChoices):
        CREATED_CASE = "created_case", "Created case"
        INGESTED_ARTIFACT = "ingested_artifact", "Ingested artifact"
        HASHED_ARTIFACT = "hashed_artifact", "Hashed artifact"
        EXTRACTED_INDICATOR = "extracted_indicator", "Extracted indicator"
        ADDED_STATEMENT = "added_statement", "Added statement"
        GENERATED_REPORT = "generated_report", "Generated report"
        REVIEWED_REPORT = "reviewed_report", "Reviewed report"
        EXPORTED_REPORT = "exported_report", "Exported report"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    case = models.ForeignKey(ScamCase, related_name="custody_events", on_delete=models.CASCADE)
    artifact = models.ForeignKey(EvidenceArtifact, null=True, blank=True, related_name="custody_events", on_delete=models.SET_NULL)
    action = models.CharField(max_length=32, choices=Action.choices)
    actor_label = models.CharField(max_length=160, default="operator")
    occurred_at = models.DateTimeField(auto_now_add=True)
    details_redacted = models.JSONField(default=dict, blank=True)
    event_hash = models.CharField(max_length=64, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=["case", "occurred_at"]),
            models.Index(fields=["artifact", "occurred_at"]),
            models.Index(fields=["event_hash"]),
        ]
        ordering = ["occurred_at"]

    def __str__(self) -> str:
        return f"{self.action} {self.event_hash[:12]}"


class GeneratedReport(models.Model):
    class ReportType(models.TextChoices):
        VICTIM = "victim", "Victim"
        AUTHORITIES = "authorities", "Authorities"
        BANK = "bank", "Bank"
        COMPANY = "company", "Company"
        TECHNICAL = "technical", "Technical"

    class Format(models.TextChoices):
        MARKDOWN = "markdown", "Markdown"

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        REVIEWED = "reviewed", "Reviewed"
        EXPORTED = "exported", "Exported"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    case = models.ForeignKey(ScamCase, related_name="reports", on_delete=models.CASCADE)
    report_type = models.CharField(max_length=32, choices=ReportType.choices)
    format = models.CharField(max_length=16, choices=Format.choices, default=Format.MARKDOWN)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.DRAFT)
    content_markdown = models.TextField()
    sha256 = models.CharField(max_length=64, db_index=True)
    generated_at = models.DateTimeField(auto_now=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["case", "report_type"], name="uniq_scam_report_per_case_type")]
        indexes = [
            models.Index(fields=["case", "report_type"]),
            models.Index(fields=["sha256"]),
            models.Index(fields=["generated_at"]),
        ]
        ordering = ["report_type"]

    def __str__(self) -> str:
        return f"{self.report_type} report for {self.case_id}"


class CaseCorrelation(models.Model):
    class CorrelationType(models.TextChoices):
        SHARED_DOMAIN = "shared_domain", "Shared domain"
        SHARED_URL_PATTERN = "shared_url_pattern", "Shared URL pattern"
        SHARED_PHONE = "shared_phone", "Shared phone"
        SHARED_IBAN = "shared_iban", "Shared IBAN"
        SHARED_IP = "shared_ip", "Shared IP"
        SHARED_TEXT_PATTERN = "shared_text_pattern", "Shared text pattern"
        SHARED_HASH = "shared_hash", "Shared hash"
        SHARED_CAMPAIGN = "shared_campaign", "Shared campaign"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    source_case = models.ForeignKey(ScamCase, related_name="outgoing_correlations", on_delete=models.CASCADE)
    target_case = models.ForeignKey(ScamCase, related_name="incoming_correlations", on_delete=models.CASCADE)
    correlation_type = models.CharField(max_length=32, choices=CorrelationType.choices)
    score = models.FloatField(default=0.0)
    explanation = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["source_case", "target_case", "correlation_type"], name="uniq_scam_case_correlation")]
        indexes = [
            models.Index(fields=["source_case", "created_at"]),
            models.Index(fields=["target_case", "created_at"]),
            models.Index(fields=["correlation_type"]),
            models.Index(fields=["created_at"]),
        ]
        ordering = ["-score", "-created_at"]

    def __str__(self) -> str:
        return f"{self.correlation_type} {self.score:.2f}"
