from __future__ import annotations

import hashlib
import re
from typing import Any
from urllib.parse import urlparse

from django.core.exceptions import ValidationError
from django.db import transaction

from source_registry.models import DataSource, DataSourceAuditEvent


SECRET_PATTERNS = (
    re.compile(r"password\s*=", re.IGNORECASE),
    re.compile(r"token\s*=", re.IGNORECASE),
    re.compile(r"api_key\s*=", re.IGNORECASE),
    re.compile(r"secret\s*=", re.IGNORECASE),
    re.compile(r"\bBearer\b", re.IGNORECASE),
)

URI_SCHEMES_WITH_USERINFO_RISK = {"ftp", "ftps", "http", "https", "sftp", "smb", "ssh", "webdav", "webdavs"}


def compute_locator_hash(locator_ref: str) -> str:
    normalized = (locator_ref or "").strip()
    if not normalized:
        return ""
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def locator_display(locator_ref: str) -> str:
    normalized = (locator_ref or "").strip()
    if not normalized:
        return ""

    parsed = urlparse(normalized)
    if parsed.scheme and parsed.netloc:
        host = parsed.hostname or parsed.netloc.rsplit("@", 1)[-1]
        path_tail = parsed.path.rstrip("/").rsplit("/", 1)[-1] if parsed.path.rstrip("/") else ""
        suffix = f"/.../{path_tail}" if path_tail else "/..."
        return f"{parsed.scheme}://{host}{suffix}"

    if normalized.startswith("//"):
        parts = [part for part in normalized.strip("/").split("/") if part]
        if len(parts) >= 2:
            return f"//{parts[0]}/.../{parts[-1]}"
        return normalized

    if "/" in normalized:
        tail = normalized.rstrip("/").rsplit("/", 1)[-1]
        return f".../{tail}" if tail else "..."

    if "\\" in normalized:
        tail = normalized.rstrip("\\").rsplit("\\", 1)[-1]
        return f"...\\{tail}" if tail else "..."

    if len(normalized) > 80:
        return f"{normalized[:32]}...{normalized[-16:]}"
    return normalized


def _ensure_no_userinfo_uri(value: str, field: str) -> None:
    parsed = urlparse(value)
    if parsed.scheme.lower() in URI_SCHEMES_WITH_USERINFO_RISK and (parsed.username or parsed.password):
        raise ValidationError({field: "Cette URI contient des identifiants. Ne saisissez aucun utilisateur, mot de passe ni token dans le locator."})


def _ensure_no_secret(value: Any, field: str) -> None:
    if value is None:
        return
    text = str(value)
    for pattern in SECRET_PATTERNS:
        if pattern.search(text):
            raise ValidationError({field: "Cette valeur ressemble à un secret. Ne saisissez aucun mot de passe ni token."})
    _ensure_no_userinfo_uri(text, field)


def _clean_exclusions(value: Any) -> list[str]:
    if value in (None, ""):
        return []
    if isinstance(value, str):
        raw_items = [line.strip() for line in value.splitlines()]
    elif isinstance(value, list):
        raw_items = [str(item).strip() for item in value]
    else:
        raise ValidationError({"exclusions": "Les exclusions doivent être une liste de textes."})
    items = [item for item in raw_items if item]
    for item in items:
        _ensure_no_secret(item, "exclusions")
    return items


def validate_source_input(input_data: dict[str, Any], *, partial: bool = False) -> dict[str, Any]:
    cleaned: dict[str, Any] = {}

    if not partial or "label" in input_data:
        label = str(input_data.get("label", "")).strip()
        if not label:
            raise ValidationError({"label": "Le nom de la source est obligatoire."})
        _ensure_no_secret(label, "label")
        cleaned["label"] = label

    if not partial or "source_type" in input_data:
        source_type = str(input_data.get("source_type", "")).strip()
        valid_types = {choice.value for choice in DataSource.SourceType}
        if source_type not in valid_types:
            raise ValidationError({"source_type": "Le type de source est obligatoire."})
        cleaned["source_type"] = source_type

    if "locator_ref" in input_data or not partial:
        locator_ref = str(input_data.get("locator_ref", "")).strip()
        _ensure_no_secret(locator_ref, "locator_ref")
        cleaned["locator_ref"] = locator_ref
        cleaned["locator_hash"] = compute_locator_hash(locator_ref)

    if "read_only" in input_data and input_data.get("read_only") is not True:
        raise ValidationError({"read_only": "Le mode lecture seule est obligatoire en v0.1."})
    cleaned["read_only"] = True

    if "include_hidden" in input_data:
        cleaned["include_hidden"] = bool(input_data.get("include_hidden"))
    elif not partial:
        cleaned["include_hidden"] = True

    if "follow_symlinks" in input_data and input_data.get("follow_symlinks"):
        raise ValidationError({"follow_symlinks": "Le suivi des liens symboliques reste désactivé en v0.1."})
    cleaned["follow_symlinks"] = False

    if "exclusions" in input_data or not partial:
        cleaned["exclusions"] = _clean_exclusions(input_data.get("exclusions", []))

    if "notes_redacted" in input_data or not partial:
        notes_redacted = str(input_data.get("notes_redacted", "")).strip()
        _ensure_no_secret(notes_redacted, "notes_redacted")
        cleaned["notes_redacted"] = notes_redacted

    return cleaned


def _audit(source: DataSource, event_type: str, *, actor_label: str | None = None, details_redacted: dict[str, Any] | None = None) -> None:
    DataSourceAuditEvent.objects.create(
        source=source,
        event_type=event_type,
        actor_label=actor_label or "",
        details_redacted=details_redacted or {},
    )


def list_data_sources(*, organization=None, include_unscoped: bool = False):
    queryset = DataSource.objects.prefetch_related("audit_events").all()
    if organization is not None:
        queryset = queryset.filter(organization=organization) | (queryset.filter(organization__isnull=True) if include_unscoped else DataSource.objects.none())
    return queryset


def create_data_source(input_data: dict[str, Any], *, organization=None) -> DataSource:
    cleaned = validate_source_input(input_data)
    if organization is not None:
        cleaned["organization"] = organization
    with transaction.atomic():
        source = DataSource.objects.create(**cleaned)
        _audit(source, DataSourceAuditEvent.EventType.CREATED, details_redacted={"source_type": source.source_type})
    return source


def update_data_source(id: str, input_data: dict[str, Any], *, organization=None) -> DataSource:
    cleaned = validate_source_input(input_data, partial=True)
    with transaction.atomic():
        queryset = DataSource.objects.select_for_update()
        if organization is not None:
            queryset = queryset.filter(organization=organization)
        source = queryset.get(id=id)
        for field, value in cleaned.items():
            setattr(source, field, value)
        source.save()
        _audit(source, DataSourceAuditEvent.EventType.UPDATED, details_redacted={"updated_fields": sorted(cleaned)})
    return source


def mark_data_source_ready(id: str, *, organization=None) -> DataSource:
    with transaction.atomic():
        queryset = DataSource.objects.select_for_update()
        if organization is not None:
            queryset = queryset.filter(organization=organization)
        source = queryset.get(id=id)
        if not source.label or not source.source_type:
            raise ValidationError("La source doit avoir un nom et un type.")
        source.status = DataSource.Status.READY
        source.save(update_fields=["status", "updated_at"])
        _audit(source, DataSourceAuditEvent.EventType.MARKED_READY)
    return source


def disable_data_source(id: str, *, organization=None) -> DataSource:
    with transaction.atomic():
        queryset = DataSource.objects.select_for_update()
        if organization is not None:
            queryset = queryset.filter(organization=organization)
        source = queryset.get(id=id)
        source.status = DataSource.Status.DISABLED
        source.save(update_fields=["status", "updated_at"])
        _audit(source, DataSourceAuditEvent.EventType.DISABLED)
    return source
