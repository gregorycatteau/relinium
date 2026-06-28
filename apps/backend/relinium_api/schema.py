from __future__ import annotations

from enum import Enum
from typing import Any

import strawberry
from django.contrib.auth import logout as django_logout
from django.core.exceptions import PermissionDenied, ValidationError
from graphql import GraphQLError
from strawberry.scalars import JSON
from strawberry.types import Info

from accounts import permissions as auth_permissions
from accounts import services as auth_services
from accounts.models import AccessRequest as AccessRequestModel
from accounts.models import Organization as OrganizationModel
from accounts.models import OrganizationMembership, UserProfile
from cockpit import services
from scam_trace import services as scam_services
from scam_trace.models import CaseCorrelation, EvidenceArtifact, GeneratedReport, ScamCase, ScamQuestionnaireAnswer, TechnicalIndicator, TimelineEvent
from source_registry import services as source_services
from source_registry.models import DataSource as DataSourceModel
from source_registry.models import DataSourceAuditEvent as DataSourceAuditEventModel


DEFAULT_LIMIT = 50
MAX_LIMIT = 200


@strawberry.enum
class HashStatus(Enum):
    HASH_OK = "hash_ok"
    BASELINE = "baseline"
    ANOMALY = "anomaly"
    UNCHECKED = "unchecked"


@strawberry.enum
class DataSourceType(Enum):
    LOCAL_FOLDER = "local_folder"
    NETWORK_SHARE = "network_share"
    SERVER = "server"
    CLOUD_GED = "cloud_ged"
    OTHER = "other"


@strawberry.enum
class DataSourceStatus(Enum):
    DRAFT = "draft"
    READY = "ready"
    OBSERVED = "observed"
    ERROR = "error"
    DISABLED = "disabled"


@strawberry.type
class Health:
    status: str
    ssot_root: str
    baseline_path: str
    validator_path: str


@strawberry.type
class ValidationFinding:
    severity: str
    location: str
    code: str
    message: str
    stream_path: str | None = None
    line_number: int | None = None
    event_id: str | None = None
    raw_line_sha256: str | None = None
    formatted: str | None = None


@strawberry.type
class KnownFinding:
    stream_path: str
    line: int
    code: str
    event_id: str | None
    message_fragment: str
    raw_line_sha256: str


@strawberry.type
class ValidationModeStatus:
    status: str
    finding_count: int
    matched_baseline_count: int | None
    findings: list[ValidationFinding]


@strawberry.type
class ValidationStatus:
    strict: ValidationModeStatus
    with_baseline: ValidationModeStatus
    known_findings: list[KnownFinding]


@strawberry.type
class ValidationSummary:
    strict_status: str
    with_baseline_status: str
    strict_finding_count: int
    known_finding_count: int
    matched_baseline_count: int


@strawberry.type
class CountSummary:
    streams: int
    events: int
    documents: int


@strawberry.type
class RoadmapItem:
    label: str
    progress: int
    status: str


@strawberry.type
class SsotSummary:
    ssot_root: str
    baseline_path: str
    validator_path: str
    validation: ValidationSummary
    counts: CountSummary
    roadmap: list[RoadmapItem]


@strawberry.type
class EventValidation:
    status: HashStatus
    actual_hash: str | None = None
    finding: ValidationFinding | None = None


@strawberry.type
class SsotEvent:
    id: str
    kind: str
    event_type: str
    timestamp: str
    tenant_id: str
    actor_human: str
    actor_agent: str
    path: str | None
    hash_sha256: str | None
    genesis: bool | None
    comment: str | None
    line: int
    stream_path: str
    raw_line_sha256: str
    validation: EventValidation | None


@strawberry.type
class SsotEventConnection:
    count: int
    limit: int
    offset: int
    items: list[SsotEvent]


@strawberry.type
class EventStream:
    path: str
    tenant: str
    event_count: int
    kinds: JSON
    last_event: SsotEvent | None


@strawberry.type
class SsotDocument:
    path: str
    exists: bool
    declared_hash: str | None
    actual_hash: str | None
    hash_status: str
    referenced_by: str | None
    event_line: int | None
    stream_path: str | None


@strawberry.type
class SsotDocumentConnection:
    count: int
    limit: int
    offset: int
    items: list[SsotDocument]


@strawberry.type
class ScamCustodyEventType:
    id: str
    action: str
    actor_label: str
    occurred_at: str
    event_hash: str
    details_redacted: JSON


@strawberry.type
class ScamCaseType:
    id: str
    title: str
    status: str
    severity: str
    initial_vector: str
    victim_type: str
    victim_label_redacted: str
    summary: str
    operator_notes_redacted: str
    discovered_at: str | None
    created_at: str
    updated_at: str
    custody_events: list[ScamCustodyEventType]


@strawberry.type
class EvidenceArtifactType:
    id: str
    case_id: str
    artifact_type: str
    original_filename_redacted: str | None
    sha256: str
    size_bytes: int | None
    storage_ref: str | None
    ingested_at: str
    source_description: str
    integrity_status: str
    metadata_redacted: JSON
    raw_content_storage_allowed: bool


@strawberry.type
class ScamQuestionnaireItem:
    key: str
    label: str
    answer_type: str
    why: str
    action: str


@strawberry.type
class ScamQuestionnaireAnswerType:
    id: str
    case_id: str
    question_key: str
    answer_type: str
    answer_value_redacted: JSON
    answered_at: str
    confidence: float
    notes_redacted: str


@strawberry.type
class TechnicalIndicatorType:
    id: str
    case_id: str
    indicator_type: str
    value_redacted: str
    value_hash: str
    first_seen_at: str
    source_artifact_id: str | None
    risk_level: str
    confidence: float
    notes_redacted: str


@strawberry.type
class TimelineEventType:
    id: str
    case_id: str
    occurred_at: str | None
    event_type: str
    label: str
    description_redacted: str
    source: str
    confidence: float
    related_artifact_id: str | None
    created_at: str


@strawberry.type
class GeneratedReportType:
    id: str
    case_id: str
    report_type: str
    format: str
    status: str
    content_markdown: str
    sha256: str
    generated_at: str
    reviewed_at: str | None


@strawberry.type
class CaseCorrelationType:
    id: str
    source_case_id: str
    target_case_id: str
    target_case_title: str
    correlation_type: str
    score: float
    explanation: str
    created_at: str


@strawberry.type
class DataSourceAuditEvent:
    id: str
    event_type: str
    actor_label: str | None
    details_redacted: JSON
    created_at: str


@strawberry.type
class DataSource:
    id: str
    label: str
    source_type: DataSourceType
    status: DataSourceStatus
    locator_ref: str
    locator_hash: str
    read_only: bool
    include_hidden: bool
    follow_symlinks: bool
    exclusions: list[str]
    notes_redacted: str
    last_observed_at: str | None
    created_at: str
    updated_at: str
    audit_events: list[DataSourceAuditEvent]


@strawberry.type
class Organization:
    id: str
    slug: str
    name: str
    status: str
    mfa_policy: str


@strawberry.type
class Membership:
    id: str
    organization: Organization
    role: str
    status: str
    created_at: str


@strawberry.type
class CurrentUser:
    id: str
    email_redacted: str
    display_name: str
    avatar_initials: str
    locale: str
    timezone: str
    mfa_required: bool
    mfa_enrolled: bool
    selected_organization: Organization | None


@strawberry.type
class AuthStatus:
    authenticated: bool
    mode: str
    oidc_configured: bool
    dev_auth_enabled: bool
    mfa_required: bool
    mfa_enrolled: bool
    user: CurrentUser | None
    current_organization: Organization | None
    permissions: list[str]


@strawberry.type
class PermissionSet:
    organization: Organization | None
    permissions: list[str]


@strawberry.type
class AccessRequest:
    id: str
    email_redacted: str
    organization_hint: str
    requested_role: str
    status: str
    requested_at: str


@strawberry.type
class AddScamArtifactResult:
    artifact: EvidenceArtifactType
    custody_events: list[ScamCustodyEventType]
    indicators: list[TechnicalIndicatorType]


@strawberry.input
class CreateScamCaseInput:
    title: str
    initial_vector: str = "other"
    victim_type: str = "unknown"
    victim_label_redacted: str = ""
    summary: str = ""
    operator_notes_redacted: str = ""


@strawberry.input
class AddScamArtifactInput:
    case_id: str
    artifact_type: str
    raw_text: str = ""
    sha256: str = ""
    original_filename_redacted: str = ""
    source_description: str = ""


@strawberry.input
class AnswerScamQuestionInput:
    case_id: str
    question_key: str
    value: JSON
    notes_redacted: str = ""
    confidence: float = 0.8


@strawberry.input
class CreateDataSourceInput:
    label: str
    source_type: DataSourceType
    locator_ref: str = ""
    include_hidden: bool = True
    exclusions: list[str] = strawberry.field(default_factory=list)
    notes_redacted: str = ""


@strawberry.input
class UpdateDataSourceInput:
    label: str | None = None
    source_type: DataSourceType | None = None
    locator_ref: str | None = None
    include_hidden: bool | None = None
    exclusions: list[str] | None = None
    notes_redacted: str | None = None


@strawberry.input
class RequestAccessInput:
    email: str
    organization_hint: str = ""
    requested_role: str = "viewer"
    message_redacted: str = ""


@strawberry.input
class UpdateMyProfileInput:
    display_name: str = ""
    locale: str = "fr-FR"
    timezone: str = "Europe/Paris"


def request_from_info(info: Info):
    context = info.context
    return getattr(context, "request", context)


def graphql_error(error: Exception) -> GraphQLError:
    if isinstance(error, PermissionDenied):
        return GraphQLError(str(error) or "Permission insuffisante.")
    if isinstance(error, ValidationError):
        messages = []
        if hasattr(error, "message_dict"):
            for field, field_messages in error.message_dict.items():
                for message in field_messages:
                    messages.append(f"{field}: {message}")
        else:
            messages = [str(message) for message in error.messages]
        return GraphQLError(" ".join(messages) or "Entrée invalide.")
    return GraphQLError("Opération impossible.")


def current_user_from_info(info: Info):
    return auth_services.effective_user(request_from_info(info))


def current_organization_from_user(user):
    return auth_permissions.get_user_organization(user)


def require_graphql_permission(info: Info, permission_code: str):
    user = current_user_from_info(info)
    organization = current_organization_from_user(user)
    try:
        auth_permissions.require_permission(user, organization, permission_code)
    except PermissionDenied as error:
        raise graphql_error(error) from None
    return user, organization


def bounded_slice(items: list[Any], limit: int, offset: int) -> tuple[list[Any], int, int]:
    safe_limit = min(max(limit, 1), MAX_LIMIT)
    safe_offset = max(offset, 0)
    return items[safe_offset : safe_offset + safe_limit], safe_limit, safe_offset


def validation_finding_from_dict(data: dict[str, Any] | None) -> ValidationFinding | None:
    if not data:
        return None
    return ValidationFinding(
        severity=str(data.get("severity", "")),
        location=str(data.get("location", "")),
        code=str(data.get("code", "")),
        message=str(data.get("message", "")),
        stream_path=data.get("stream_path"),
        line_number=data.get("line_number"),
        event_id=data.get("event_id"),
        raw_line_sha256=data.get("raw_line_sha256"),
        formatted=data.get("formatted"),
    )


def event_validation_from_dict(data: dict[str, Any] | None) -> EventValidation | None:
    if not data:
        return None
    status = data.get("status") if data.get("status") in {item.value for item in HashStatus} else "unchecked"
    return EventValidation(
        status=HashStatus(status),
        actual_hash=data.get("actual_hash"),
        finding=validation_finding_from_dict(data.get("finding")),
    )


def event_from_dict(data: dict[str, Any] | None) -> SsotEvent | None:
    if not data:
        return None
    return SsotEvent(
        id=str(data.get("id", "")),
        kind=str(data.get("kind", "")),
        event_type=str(data.get("event_type", "")),
        timestamp=str(data.get("timestamp", "")),
        tenant_id=str(data.get("tenant_id", "")),
        actor_human=str(data.get("actor_human", "")),
        actor_agent=str(data.get("actor_agent", "")),
        path=data.get("path"),
        hash_sha256=data.get("hash_sha256"),
        genesis=data.get("genesis"),
        comment=data.get("comment"),
        line=int(data.get("line", 0)),
        stream_path=str(data.get("stream_path", "")),
        raw_line_sha256=str(data.get("raw_line_sha256", "")),
        validation=event_validation_from_dict(data.get("validation")),
    )


def validation_status_from_dict(data: dict[str, Any]) -> ValidationStatus:
    strict = data["strict"]
    with_baseline = data["with_baseline"]
    known = data["known_findings"].get("findings", [])
    return ValidationStatus(
        strict=ValidationModeStatus(
            status=strict["status"],
            finding_count=strict["finding_count"],
            matched_baseline_count=None,
            findings=[item for item in (validation_finding_from_dict(finding) for finding in strict["findings"]) if item],
        ),
        with_baseline=ValidationModeStatus(
            status=with_baseline["status"],
            finding_count=with_baseline["finding_count"],
            matched_baseline_count=with_baseline["matched_baseline_count"],
            findings=[item for item in (validation_finding_from_dict(finding) for finding in with_baseline["findings"]) if item],
        ),
        known_findings=[
            KnownFinding(
                stream_path=str(item.get("stream_path", "")),
                line=int(item.get("line", 0)),
                code=str(item.get("code", "")),
                event_id=item.get("event_id"),
                message_fragment=str(item.get("message_fragment", "")),
                raw_line_sha256=str(item.get("raw_line_sha256", "")),
            )
            for item in known
            if isinstance(item, dict)
        ],
    )


def summary_from_dict(data: dict[str, Any]) -> SsotSummary:
    return SsotSummary(
        ssot_root=data["ssot_root"],
        baseline_path=data["baseline_path"],
        validator_path=data["validator_path"],
        validation=ValidationSummary(**data["validation"]),
        counts=CountSummary(**data["counts"]),
        roadmap=[RoadmapItem(**item) for item in data["roadmap"]],
    )


def scam_custody_from_model(item) -> ScamCustodyEventType:
    return ScamCustodyEventType(
        id=str(item.id),
        action=item.action,
        actor_label=item.actor_label,
        occurred_at=item.occurred_at.isoformat(),
        event_hash=item.event_hash,
        details_redacted=item.details_redacted,
    )


def scam_case_from_model(item: ScamCase) -> ScamCaseType:
    return ScamCaseType(
        id=str(item.id),
        title=item.title,
        status=item.status,
        severity=item.severity,
        initial_vector=item.initial_vector,
        victim_type=item.victim_type,
        victim_label_redacted=item.victim_label_redacted,
        summary=item.summary,
        operator_notes_redacted=item.operator_notes_redacted,
        discovered_at=item.discovered_at.isoformat() if item.discovered_at else None,
        created_at=item.created_at.isoformat(),
        updated_at=item.updated_at.isoformat(),
        custody_events=[scam_custody_from_model(event) for event in item.custody_events.all()[:20]],
    )


def scam_artifact_from_model(item: EvidenceArtifact) -> EvidenceArtifactType:
    return EvidenceArtifactType(
        id=str(item.id),
        case_id=str(item.case_id),
        artifact_type=item.artifact_type,
        original_filename_redacted=item.original_filename_redacted,
        sha256=item.sha256,
        size_bytes=item.size_bytes,
        storage_ref=item.storage_ref,
        ingested_at=item.ingested_at.isoformat(),
        source_description=item.source_description,
        integrity_status=item.integrity_status,
        metadata_redacted=item.metadata_redacted,
        raw_content_storage_allowed=item.raw_content_storage_allowed,
    )


def scam_answer_from_model(item: ScamQuestionnaireAnswer) -> ScamQuestionnaireAnswerType:
    return ScamQuestionnaireAnswerType(
        id=str(item.id),
        case_id=str(item.case_id),
        question_key=item.question_key,
        answer_type=item.answer_type,
        answer_value_redacted=item.answer_value_redacted,
        answered_at=item.answered_at.isoformat(),
        confidence=item.confidence,
        notes_redacted=item.notes_redacted,
    )


def scam_indicator_from_model(item: TechnicalIndicator) -> TechnicalIndicatorType:
    return TechnicalIndicatorType(
        id=str(item.id),
        case_id=str(item.case_id),
        indicator_type=item.indicator_type,
        value_redacted=item.value_redacted,
        value_hash=item.value_hash,
        first_seen_at=item.first_seen_at.isoformat(),
        source_artifact_id=str(item.source_artifact_id) if item.source_artifact_id else None,
        risk_level=item.risk_level,
        confidence=item.confidence,
        notes_redacted=item.notes_redacted,
    )


def scam_timeline_from_model(item: TimelineEvent) -> TimelineEventType:
    return TimelineEventType(
        id=str(item.id),
        case_id=str(item.case_id),
        occurred_at=item.occurred_at.isoformat() if item.occurred_at else None,
        event_type=item.event_type,
        label=item.label,
        description_redacted=item.description_redacted,
        source=item.source,
        confidence=item.confidence,
        related_artifact_id=str(item.related_artifact_id) if item.related_artifact_id else None,
        created_at=item.created_at.isoformat(),
    )


def scam_report_from_model(item: GeneratedReport) -> GeneratedReportType:
    return GeneratedReportType(
        id=str(item.id),
        case_id=str(item.case_id),
        report_type=item.report_type,
        format=item.format,
        status=item.status,
        content_markdown=item.content_markdown,
        sha256=item.sha256,
        generated_at=item.generated_at.isoformat(),
        reviewed_at=item.reviewed_at.isoformat() if item.reviewed_at else None,
    )


def scam_correlation_from_model(item: CaseCorrelation) -> CaseCorrelationType:
    return CaseCorrelationType(
        id=str(item.id),
        source_case_id=str(item.source_case_id),
        target_case_id=str(item.target_case_id),
        target_case_title=item.target_case.title,
        correlation_type=item.correlation_type,
        score=item.score,
        explanation=item.explanation,
        created_at=item.created_at.isoformat(),
    )


def data_source_audit_from_model(item: DataSourceAuditEventModel) -> DataSourceAuditEvent:
    return DataSourceAuditEvent(
        id=str(item.id),
        event_type=item.event_type,
        actor_label=item.actor_label,
        details_redacted=item.details_redacted,
        created_at=item.created_at.isoformat(),
    )


def data_source_from_model(item: DataSourceModel) -> DataSource:
    return DataSource(
        id=str(item.id),
        label=item.label,
        source_type=DataSourceType(item.source_type),
        status=DataSourceStatus(item.status),
        locator_ref=item.locator_ref,
        locator_hash=item.locator_hash,
        read_only=item.read_only,
        include_hidden=item.include_hidden,
        follow_symlinks=item.follow_symlinks,
        exclusions=item.exclusions if isinstance(item.exclusions, list) else [],
        notes_redacted=item.notes_redacted,
        last_observed_at=item.last_observed_at.isoformat() if item.last_observed_at else None,
        created_at=item.created_at.isoformat(),
        updated_at=item.updated_at.isoformat(),
        audit_events=[data_source_audit_from_model(event) for event in item.audit_events.all()[:20]],
    )


def organization_from_model(item: OrganizationModel | None) -> Organization | None:
    if item is None:
        return None
    return Organization(id=str(item.id), slug=item.slug, name=item.name, status=item.status, mfa_policy=item.mfa_policy)


def membership_from_model(item: OrganizationMembership) -> Membership:
    return Membership(
        id=str(item.id),
        organization=organization_from_model(item.organization),
        role=item.role,
        status=item.status,
        created_at=item.created_at.isoformat(),
    )


def current_user_from_model(user) -> CurrentUser | None:
    if not getattr(user, "is_authenticated", False):
        return None
    profile: UserProfile = auth_services.ensure_profile(user)
    return CurrentUser(
        id=str(user.id),
        email_redacted=auth_services.redact_email(user.email or user.get_username()),
        display_name=profile.display_name,
        avatar_initials=profile.avatar_initials,
        locale=profile.locale,
        timezone=profile.timezone,
        mfa_required=profile.mfa_required,
        mfa_enrolled=profile.mfa_enrolled,
        selected_organization=organization_from_model(profile.selected_organization),
    )


def auth_status_from_dict(data: dict[str, Any]) -> AuthStatus:
    return AuthStatus(
        authenticated=data["authenticated"],
        mode=data["mode"],
        oidc_configured=data["oidc_configured"],
        dev_auth_enabled=data["dev_auth_enabled"],
        mfa_required=data["mfa_required"],
        mfa_enrolled=data["mfa_enrolled"],
        user=current_user_from_model(data["user"]),
        current_organization=organization_from_model(data["organization"]),
        permissions=data["permissions"],
    )


def access_request_from_model(item: AccessRequestModel) -> AccessRequest:
    return AccessRequest(
        id=str(item.id),
        email_redacted=item.email_redacted,
        organization_hint=item.organization_hint,
        requested_role=item.requested_role,
        status=item.status,
        requested_at=item.requested_at.isoformat(),
    )


def create_data_source_input_to_dict(input: CreateDataSourceInput) -> dict[str, Any]:
    return {
        "label": input.label,
        "source_type": input.source_type.value,
        "locator_ref": input.locator_ref,
        "include_hidden": input.include_hidden,
        "exclusions": input.exclusions,
        "notes_redacted": input.notes_redacted,
        "read_only": True,
        "follow_symlinks": False,
    }


def update_data_source_input_to_dict(input: UpdateDataSourceInput) -> dict[str, Any]:
    data: dict[str, Any] = {}
    if input.label is not None:
        data["label"] = input.label
    if input.source_type is not None:
        data["source_type"] = input.source_type.value
    if input.locator_ref is not None:
        data["locator_ref"] = input.locator_ref
    if input.include_hidden is not None:
        data["include_hidden"] = input.include_hidden
    if input.exclusions is not None:
        data["exclusions"] = input.exclusions
    if input.notes_redacted is not None:
        data["notes_redacted"] = input.notes_redacted
    data["read_only"] = True
    data["follow_symlinks"] = False
    return data


@strawberry.type
class Query:
    @strawberry.field
    def auth_status(self, info: Info) -> AuthStatus:
        return auth_status_from_dict(auth_services.get_auth_status(request_from_info(info)))

    @strawberry.field
    def current_user(self, info: Info) -> CurrentUser | None:
        return current_user_from_model(current_user_from_info(info))

    @strawberry.field
    def current_organization(self, info: Info) -> Organization | None:
        return organization_from_model(current_organization_from_user(current_user_from_info(info)))

    @strawberry.field
    def my_memberships(self, info: Info) -> list[Membership]:
        user = current_user_from_info(info)
        if not getattr(user, "is_authenticated", False):
            return []
        return [
            membership_from_model(item)
            for item in OrganizationMembership.objects.select_related("organization")
            .filter(user=user)
            .order_by("organization__name")
        ]

    @strawberry.field
    def my_permissions(self, info: Info) -> PermissionSet:
        user = current_user_from_info(info)
        organization = current_organization_from_user(user)
        return PermissionSet(
            organization=organization_from_model(organization),
            permissions=sorted(auth_permissions.get_user_permissions(user, organization)),
        )

    @strawberry.field
    def health(self) -> Health:
        return Health(status="ok", **services.json_response_data())

    @strawberry.field
    def ssot_summary(self) -> SsotSummary:
        return summary_from_dict(services.collect_summary())

    @strawberry.field
    def event_streams(self) -> list[EventStream]:
        return [
            EventStream(
                path=item["path"],
                tenant=item["tenant"],
                event_count=item["event_count"],
                kinds=item["kinds"],
                last_event=event_from_dict(item.get("last_event")),
            )
            for item in services.collect_streams()
        ]

    @strawberry.field
    def events(self, limit: int = DEFAULT_LIMIT, offset: int = 0, status: HashStatus | None = None) -> SsotEventConnection:
        events_data = services.collect_events()["events"]
        if status:
            events_data = [item for item in events_data if item.get("validation", {}).get("status") == status.value]
        items, safe_limit, safe_offset = bounded_slice(events_data, limit, offset)
        return SsotEventConnection(
            count=len(events_data),
            limit=safe_limit,
            offset=safe_offset,
            items=[item for item in (event_from_dict(event) for event in items) if item],
        )

    @strawberry.field
    def validation_status(self) -> ValidationStatus:
        return validation_status_from_dict(services.collect_validation())

    @strawberry.field
    def known_findings(self) -> list[KnownFinding]:
        return validation_status_from_dict(services.collect_validation()).known_findings

    @strawberry.field
    def documents(self, limit: int = DEFAULT_LIMIT, offset: int = 0) -> SsotDocumentConnection:
        documents_data = services.collect_documents()["documents"]
        items, safe_limit, safe_offset = bounded_slice(documents_data, limit, offset)
        return SsotDocumentConnection(
            count=len(documents_data),
            limit=safe_limit,
            offset=safe_offset,
            items=[
                SsotDocument(
                    path=item["path"],
                    exists=item["exists"],
                    declared_hash=item.get("declared_hash"),
                    actual_hash=item.get("actual_hash"),
                    hash_status=item["hash_status"],
                    referenced_by=item.get("referenced_by"),
                    event_line=item.get("event_line"),
                    stream_path=item.get("stream_path"),
                )
                for item in items
            ],
        )

    @strawberry.field
    def roadmap_status(self) -> list[RoadmapItem]:
        return [RoadmapItem(**item) for item in services.collect_summary()["roadmap"]]

    @strawberry.field
    def scam_cases(self, info: Info) -> list[ScamCaseType]:
        _, organization = require_graphql_permission(info, auth_permissions.PERMISSION_SCAM_CASE_READ)
        queryset = ScamCase.objects.prefetch_related("custody_events").filter(organization=organization)
        return [scam_case_from_model(item) for item in queryset[:100]]

    @strawberry.field
    def scam_case(self, info: Info, id: str) -> ScamCaseType | None:
        _, organization = require_graphql_permission(info, auth_permissions.PERMISSION_SCAM_CASE_READ)
        item = ScamCase.objects.prefetch_related("custody_events").filter(id=id, organization=organization).first()
        return scam_case_from_model(item) if item else None

    @strawberry.field
    def scam_case_timeline(self, info: Info, case_id: str) -> list[TimelineEventType]:
        _, organization = require_graphql_permission(info, auth_permissions.PERMISSION_SCAM_CASE_READ)
        if not ScamCase.objects.filter(id=case_id, organization=organization).exists():
            return []
        return [scam_timeline_from_model(item) for item in TimelineEvent.objects.filter(case_id=case_id)[:200]]

    @strawberry.field
    def scam_case_indicators(self, info: Info, case_id: str) -> list[TechnicalIndicatorType]:
        _, organization = require_graphql_permission(info, auth_permissions.PERMISSION_SCAM_CASE_READ)
        if not ScamCase.objects.filter(id=case_id, organization=organization).exists():
            return []
        return [scam_indicator_from_model(item) for item in TechnicalIndicator.objects.filter(case_id=case_id)[:200]]

    @strawberry.field
    def scam_case_reports(self, info: Info, case_id: str) -> list[GeneratedReportType]:
        _, organization = require_graphql_permission(info, auth_permissions.PERMISSION_SCAM_CASE_READ)
        if not ScamCase.objects.filter(id=case_id, organization=organization).exists():
            return []
        return [scam_report_from_model(item) for item in GeneratedReport.objects.filter(case_id=case_id)[:20]]

    @strawberry.field
    def scam_case_correlations(self, info: Info, case_id: str) -> list[CaseCorrelationType]:
        _, organization = require_graphql_permission(info, auth_permissions.PERMISSION_SCAM_CASE_READ)
        if not ScamCase.objects.filter(id=case_id, organization=organization).exists():
            return []
        return [scam_correlation_from_model(item) for item in CaseCorrelation.objects.select_related("target_case").filter(source_case_id=case_id)[:100]]

    @strawberry.field
    def scam_questionnaire_template(self) -> list[ScamQuestionnaireItem]:
        return [
            ScamQuestionnaireItem(
                key=item["key"],
                label=item["label"],
                answer_type=item["answerType"],
                why=item["why"],
                action=item["action"],
            )
            for item in scam_services.QUESTIONNAIRE_TEMPLATE
        ]

    @strawberry.field
    def data_sources(self, info: Info) -> list[DataSource]:
        _, organization = require_graphql_permission(info, auth_permissions.PERMISSION_SOURCE_READ)
        include_unscoped = auth_services.get_auth_status(request_from_info(info))["mode"] == "dev"
        return [data_source_from_model(item) for item in source_services.list_data_sources(organization=organization, include_unscoped=include_unscoped)]

    @strawberry.field
    def data_source(self, info: Info, id: str) -> DataSource | None:
        _, organization = require_graphql_permission(info, auth_permissions.PERMISSION_SOURCE_READ)
        item = DataSourceModel.objects.prefetch_related("audit_events").filter(id=id, organization=organization).first()
        return data_source_from_model(item) if item else None


@strawberry.type
class Mutation:
    @strawberry.mutation
    def request_access(self, info: Info, input: RequestAccessInput) -> AccessRequest:
        try:
            item = auth_services.request_access(
                {
                    "email": input.email,
                    "organization_hint": input.organization_hint,
                    "requested_role": input.requested_role,
                    "message_redacted": input.message_redacted,
                },
                request=request_from_info(info),
            )
        except (PermissionDenied, ValidationError) as error:
            raise graphql_error(error) from None
        return access_request_from_model(item)

    @strawberry.mutation
    def update_my_profile(self, info: Info, input: UpdateMyProfileInput) -> CurrentUser:
        user = current_user_from_info(info)
        try:
            auth_services.update_profile(
                user,
                {"display_name": input.display_name, "locale": input.locale, "timezone": input.timezone},
            )
        except (PermissionDenied, ValidationError) as error:
            raise graphql_error(error) from None
        return current_user_from_model(user)

    @strawberry.mutation
    def select_organization(self, info: Info, organization_id: str) -> Organization:
        user = current_user_from_info(info)
        try:
            organization = auth_services.select_organization(user, organization_id)
        except PermissionDenied as error:
            raise graphql_error(error) from None
        return organization_from_model(organization)

    @strawberry.mutation
    def logout(self, info: Info) -> AuthStatus:
        request = request_from_info(info)
        django_logout(request)
        return auth_status_from_dict(auth_services.get_auth_status(request))

    @strawberry.mutation
    def create_data_source(self, info: Info, input: CreateDataSourceInput) -> DataSource:
        user, organization = require_graphql_permission(info, auth_permissions.PERMISSION_SOURCE_CREATE)
        source = source_services.create_data_source(create_data_source_input_to_dict(input), organization=organization)
        auth_services.audit_auth_event(
            request=request_from_info(info),
            actor_user=user,
            organization=organization,
            action="source_created",
            target_type="data_source",
            target_ref=str(source.id),
            metadata_redacted={"source_type": source.source_type},
        )
        return data_source_from_model(DataSourceModel.objects.prefetch_related("audit_events").get(id=source.id))

    @strawberry.mutation
    def update_data_source(self, info: Info, id: str, input: UpdateDataSourceInput) -> DataSource:
        user, organization = require_graphql_permission(info, auth_permissions.PERMISSION_SOURCE_UPDATE)
        source = source_services.update_data_source(id, update_data_source_input_to_dict(input), organization=organization)
        auth_services.audit_auth_event(request=request_from_info(info), actor_user=user, organization=organization, action="source_updated", target_type="data_source", target_ref=str(source.id))
        return data_source_from_model(DataSourceModel.objects.prefetch_related("audit_events").get(id=source.id))

    @strawberry.mutation
    def mark_data_source_ready(self, info: Info, id: str) -> DataSource:
        user, organization = require_graphql_permission(info, auth_permissions.PERMISSION_SCAN_PREPARE)
        source = source_services.mark_data_source_ready(id, organization=organization)
        auth_services.audit_auth_event(request=request_from_info(info), actor_user=user, organization=organization, action="source_marked_ready", target_type="data_source", target_ref=str(source.id))
        return data_source_from_model(DataSourceModel.objects.prefetch_related("audit_events").get(id=source.id))

    @strawberry.mutation
    def disable_data_source(self, info: Info, id: str) -> DataSource:
        user, organization = require_graphql_permission(info, auth_permissions.PERMISSION_SOURCE_DISABLE)
        source = source_services.disable_data_source(id, organization=organization)
        auth_services.audit_auth_event(request=request_from_info(info), actor_user=user, organization=organization, action="source_disabled", target_type="data_source", target_ref=str(source.id))
        return data_source_from_model(DataSourceModel.objects.prefetch_related("audit_events").get(id=source.id))

    @strawberry.mutation
    def create_scam_case(self, info: Info, input: CreateScamCaseInput) -> ScamCaseType:
        user, organization = require_graphql_permission(info, auth_permissions.PERMISSION_SCAM_CASE_CREATE)
        case = scam_services.create_case(
            {
                "title": input.title,
                "initial_vector": input.initial_vector,
                "victim_type": input.victim_type,
                "victim_label_redacted": input.victim_label_redacted,
                "summary": input.summary,
                "operator_notes_redacted": input.operator_notes_redacted,
            },
            organization=organization,
        )
        auth_services.audit_auth_event(request=request_from_info(info), actor_user=user, organization=organization, action="scam_case_created", target_type="scam_case", target_ref=str(case.id))
        return scam_case_from_model(ScamCase.objects.prefetch_related("custody_events").get(id=case.id))

    @strawberry.mutation
    def add_scam_artifact(self, info: Info, input: AddScamArtifactInput) -> AddScamArtifactResult:
        user, organization = require_graphql_permission(info, auth_permissions.PERMISSION_SCAM_CASE_UPDATE)
        if not ScamCase.objects.filter(id=input.case_id, organization=organization).exists():
            raise GraphQLError("Permission insuffisante.")
        artifact = scam_services.add_artifact(
            input.case_id,
            {
                "artifact_type": input.artifact_type,
                "raw_text": input.raw_text,
                "sha256": input.sha256,
                "original_filename_redacted": input.original_filename_redacted,
                "source_description": input.source_description,
            },
        )
        scam_services.correlate_case(input.case_id)
        auth_services.audit_auth_event(request=request_from_info(info), actor_user=user, organization=organization, action="scam_artifact_added", target_type="scam_case", target_ref=input.case_id)
        return AddScamArtifactResult(
            artifact=scam_artifact_from_model(artifact),
            custody_events=[scam_custody_from_model(item) for item in artifact.custody_events.all()],
            indicators=[scam_indicator_from_model(item) for item in TechnicalIndicator.objects.filter(case_id=input.case_id)[:200]],
        )

    @strawberry.mutation
    def answer_scam_question(self, info: Info, input: AnswerScamQuestionInput) -> ScamQuestionnaireAnswerType:
        user, organization = require_graphql_permission(info, auth_permissions.PERMISSION_SCAM_CASE_UPDATE)
        if not ScamCase.objects.filter(id=input.case_id, organization=organization).exists():
            raise GraphQLError("Permission insuffisante.")
        answer = scam_services.add_questionnaire_answer(input.case_id, input.question_key, input.value, input.notes_redacted, input.confidence)
        auth_services.audit_auth_event(request=request_from_info(info), actor_user=user, organization=organization, action="scam_question_answered", target_type="scam_case", target_ref=input.case_id, metadata_redacted={"question_key": input.question_key})
        return scam_answer_from_model(answer)

    @strawberry.mutation
    def generate_scam_reports(self, info: Info, case_id: str) -> list[GeneratedReportType]:
        user, organization = require_graphql_permission(info, auth_permissions.PERMISSION_REPORT_GENERATE)
        if not ScamCase.objects.filter(id=case_id, organization=organization).exists():
            raise GraphQLError("Permission insuffisante.")
        scam_services.correlate_case(case_id)
        auth_services.audit_auth_event(request=request_from_info(info), actor_user=user, organization=organization, action="scam_reports_generated", target_type="scam_case", target_ref=case_id)
        return [scam_report_from_model(item) for item in scam_services.generate_case_reports(case_id)]

    @strawberry.mutation
    def mark_report_reviewed(self, info: Info, report_id: str) -> GeneratedReportType:
        user, organization = require_graphql_permission(info, auth_permissions.PERMISSION_REPORT_REVIEW)
        report = GeneratedReport.objects.select_related("case").filter(id=report_id, case__organization=organization).first()
        if report is None:
            raise GraphQLError("Permission insuffisante.")
        auth_services.audit_auth_event(request=request_from_info(info), actor_user=user, organization=organization, action="scam_report_reviewed", target_type="generated_report", target_ref=report_id)
        return scam_report_from_model(scam_services.mark_report_reviewed(report_id))

schema = strawberry.Schema(query=Query, mutation=Mutation)
