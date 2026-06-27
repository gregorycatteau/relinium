from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from email import policy
from email.parser import Parser
from typing import Any
from urllib.parse import urlparse

from django.db import transaction
from django.utils import timezone

from .models import (
    CaseCorrelation,
    CustodyEvent,
    EvidenceArtifact,
    GeneratedReport,
    ScamCase,
    ScamQuestionnaireAnswer,
    TechnicalIndicator,
    TimelineEvent,
)

MAX_RAW_TEXT_BYTES = 200_000

QUESTIONNAIRE_TEMPLATE = [
    {"key": "clicked_link", "label": "La personne a-t-elle cliqué sur un lien ?", "answerType": "boolean", "why": "Permet d'évaluer l'exposition technique.", "action": "Identifier les URLs et recommander le changement de mots de passe si nécessaire."},
    {"key": "entered_password", "label": "A-t-elle saisi un mot de passe ?", "answerType": "boolean", "why": "Signale un risque de compromission de compte.", "action": "Réinitialiser le mot de passe et vérifier les sessions actives."},
    {"key": "gave_card", "label": "A-t-elle donné une carte bancaire ?", "answerType": "boolean", "why": "Déclenche une urgence bancaire.", "action": "Contacter la banque, faire opposition et surveiller les opérations."},
    {"key": "made_transfer", "label": "A-t-elle fait un virement ?", "answerType": "boolean", "why": "Documente la perte financière et l'urgence.", "action": "Contacter la banque et préparer les éléments pour autorités."},
    {"key": "installed_software", "label": "A-t-elle installé un logiciel ?", "answerType": "boolean", "why": "Peut indiquer un accès distant ou malware.", "action": "Isoler le poste et faire une analyse technique défensive."},
    {"key": "sent_documents", "label": "A-t-elle envoyé des documents ?", "answerType": "boolean", "why": "Évalue le risque d'usurpation d'identité.", "action": "Lister les documents transmis et préparer les signalements."},
    {"key": "phone_call", "label": "Y a-t-il eu un appel téléphonique ?", "answerType": "boolean", "why": "Ajoute un vecteur vocal à la chronologie.", "action": "Conserver numéro, horaires et récit sans rappeler le suspect."},
    {"key": "remote_access", "label": "Y a-t-il eu un accès distant ?", "answerType": "boolean", "why": "Indique un risque élevé sur le poste victime.", "action": "Déconnecter l'accès, préserver les traces et analyser le poste."},
    {"key": "lost_amount", "label": "Montant perdu ou engagé ?", "answerType": "number", "why": "Aide au scoring d'impact.", "action": "Comparer avec les relevés bancaires fournis."},
    {"key": "bank_contacted", "label": "La banque a-t-elle été contactée ?", "answerType": "boolean", "why": "Vérifie les mesures d'urgence.", "action": "Si non, recommander un contact immédiat."},
    {"key": "already_reported", "label": "Plainte ou signalement déjà effectué ?", "answerType": "boolean", "why": "Évite les doublons et complète le dossier.", "action": "Conserver références de plainte ou signalement."},
]

URL_RE = re.compile(r"https?://[^\s<>'\")\]]+", re.IGNORECASE)
EMAIL_RE = re.compile(r"(?<![\w.+-])[\w.+-]+@[\w.-]+\.[a-z]{2,}(?![\w.-])", re.IGNORECASE)
PHONE_RE = re.compile(r"(?:(?:\+|00)33[\s.-]?[1-9]|0[1-9])(?:[\s.-]?\d{2}){4}")
IBAN_RE = re.compile(r"\b[A-Z]{2}\d{2}[A-Z0-9]{11,30}\b", re.IGNORECASE)
IP_RE = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
HASH_RE = re.compile(r"\b[a-f0-9]{64}\b", re.IGNORECASE)
URGENCY_WORDS = ("urgent", "paiement", "compte", "carte vitale", "amende", "colis", "remboursement", "sécurité", "bloqué", "suspendu")


@dataclass(frozen=True)
class ExtractedIndicator:
    indicator_type: str
    value_redacted: str
    risk_level: str = "medium"
    confidence: float = 0.7
    notes_redacted: str = ""


def compute_text_sha256(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def hash_value(value: str) -> str:
    return compute_text_sha256(value.strip().lower())


def _custody_hash(payload: dict[str, Any]) -> str:
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    return compute_text_sha256(canonical)


def _create_custody_event(case: ScamCase, action: str, artifact: EvidenceArtifact | None = None, details: dict[str, Any] | None = None) -> CustodyEvent:
    payload = {
        "case_id": str(case.id),
        "artifact_id": str(artifact.id) if artifact else None,
        "action": action,
        "details": details or {},
        "observed_at": timezone.now().isoformat(),
    }
    return CustodyEvent.objects.create(
        case=case,
        artifact=artifact,
        action=action,
        actor_label="operator",
        details_redacted=details or {},
        event_hash=_custody_hash(payload),
    )


def create_case(input_data: dict[str, Any]) -> ScamCase:
    allowed_vectors = {choice.value for choice in ScamCase.InitialVector}
    allowed_victims = {choice.value for choice in ScamCase.VictimType}
    title = str(input_data.get("title", "")).strip()
    if not title:
        raise ValueError("title is required")
    vector = input_data.get("initial_vector") or input_data.get("initialVector") or ScamCase.InitialVector.OTHER
    victim_type = input_data.get("victim_type") or input_data.get("victimType") or ScamCase.VictimType.UNKNOWN
    if vector not in allowed_vectors:
        raise ValueError("invalid initial_vector")
    if victim_type not in allowed_victims:
        raise ValueError("invalid victim_type")
    with transaction.atomic():
        case = ScamCase.objects.create(
            title=title[:220],
            initial_vector=vector,
            victim_type=victim_type,
            victim_label_redacted=str(input_data.get("victim_label_redacted") or input_data.get("victimLabelRedacted") or "")[:220],
            summary=str(input_data.get("summary") or "")[:5000],
            operator_notes_redacted=str(input_data.get("operator_notes_redacted") or input_data.get("operatorNotesRedacted") or "")[:5000],
            status=ScamCase.Status.ACTIVE,
        )
        _create_custody_event(case, CustodyEvent.Action.CREATED_CASE, details={"title": case.title, "initial_vector": case.initial_vector})
        TimelineEvent.objects.create(case=case, event_type=TimelineEvent.EventType.DISCOVERY, label="Dossier anti-scam ouvert", description_redacted=case.summary, source=TimelineEvent.Source.OPERATOR, confidence=0.8)
        return case


def add_artifact(case_id: str, artifact_input: dict[str, Any]) -> EvidenceArtifact:
    raw_text = str(artifact_input.get("raw_text") or artifact_input.get("rawText") or "")
    if len(raw_text.encode("utf-8")) > MAX_RAW_TEXT_BYTES:
        raise ValueError("raw text exceeds MVP limit")
    artifact_type = artifact_input.get("artifact_type") or artifact_input.get("artifactType") or EvidenceArtifact.ArtifactType.OTHER
    if artifact_type not in {choice.value for choice in EvidenceArtifact.ArtifactType}:
        raise ValueError("invalid artifact_type")
    declared_sha = str(artifact_input.get("sha256") or "").strip().lower()
    computed_sha = compute_text_sha256(raw_text) if raw_text else declared_sha
    if not re.fullmatch(r"[a-f0-9]{64}", computed_sha):
        raise ValueError("sha256 or raw text is required")
    with transaction.atomic():
        case = ScamCase.objects.select_for_update().get(id=case_id)
        artifact = EvidenceArtifact.objects.create(
            case=case,
            artifact_type=artifact_type,
            original_filename_redacted=artifact_input.get("original_filename_redacted") or artifact_input.get("originalFilenameRedacted") or None,
            sha256=computed_sha,
            size_bytes=len(raw_text.encode("utf-8")) if raw_text else artifact_input.get("size_bytes") or artifact_input.get("sizeBytes"),
            storage_ref=artifact_input.get("storage_ref") or artifact_input.get("storageRef") or None,
            source_description=str(artifact_input.get("source_description") or artifact_input.get("sourceDescription") or "")[:2000],
            integrity_status=EvidenceArtifact.IntegrityStatus.HASHED if raw_text else EvidenceArtifact.IntegrityStatus.DECLARED,
            metadata_redacted={"text_sha256": computed_sha, "text_size_bytes": len(raw_text.encode("utf-8"))} if raw_text else {},
            raw_content_storage_allowed=False,
        )
        _create_custody_event(case, CustodyEvent.Action.INGESTED_ARTIFACT, artifact, {"artifact_type": artifact.artifact_type, "sha256": artifact.sha256})
        _create_custody_event(case, CustodyEvent.Action.HASHED_ARTIFACT, artifact, {"sha256": artifact.sha256, "size_bytes": artifact.size_bytes})
        TimelineEvent.objects.create(case=case, event_type=TimelineEvent.EventType.RECEIVED, label="Preuve ajoutée et hashée", description_redacted=artifact.source_description, source=TimelineEvent.Source.ARTIFACT, related_artifact=artifact, confidence=0.8)
        for indicator in extract_indicators(raw_text, artifact_type):
            _upsert_indicator(case, indicator, artifact)
        return artifact


def add_questionnaire_answer(case_id: str, question_key: str, value: Any, notes_redacted: str = "", confidence: float = 0.8) -> ScamQuestionnaireAnswer:
    if question_key not in {item["key"] for item in QUESTIONNAIRE_TEMPLATE}:
        raise ValueError("unknown question_key")
    template = next(item for item in QUESTIONNAIRE_TEMPLATE if item["key"] == question_key)
    answer_type = template["answerType"]
    payload = {"value": value}
    with transaction.atomic():
        case = ScamCase.objects.get(id=case_id)
        answer, _ = ScamQuestionnaireAnswer.objects.update_or_create(
            case=case,
            question_key=question_key,
            defaults={"answer_type": answer_type, "answer_value_redacted": payload, "confidence": max(0.0, min(float(confidence), 1.0)), "notes_redacted": notes_redacted[:2000]},
        )
        _create_custody_event(case, CustodyEvent.Action.ADDED_STATEMENT, details={"question_key": question_key, "answer_type": answer_type})
        derive_timeline_from_answers(case_id)
        return answer


def derive_timeline_from_answers(case_id: str) -> list[TimelineEvent]:
    case = ScamCase.objects.get(id=case_id)
    mapping = {
        "clicked_link": (TimelineEvent.EventType.CLICKED, "Lien suspect cliqué"),
        "entered_password": (TimelineEvent.EventType.SUBMITTED_CREDENTIALS, "Identifiants saisis"),
        "gave_card": (TimelineEvent.EventType.SUBMITTED_PAYMENT, "Données de carte bancaire communiquées"),
        "made_transfer": (TimelineEvent.EventType.TRANSFER, "Virement ou paiement réalisé"),
        "installed_software": (TimelineEvent.EventType.REMOTE_ACCESS, "Logiciel ou accès distant suspect"),
        "sent_documents": (TimelineEvent.EventType.OTHER, "Documents transmis au suspect"),
        "phone_call": (TimelineEvent.EventType.PHONE_CALL, "Appel avec le suspect"),
        "remote_access": (TimelineEvent.EventType.REMOTE_ACCESS, "Accès distant déclaré"),
        "bank_contacted": (TimelineEvent.EventType.REMEDIATION, "Banque contactée"),
        "already_reported": (TimelineEvent.EventType.REPORT, "Signalement ou plainte déjà effectué"),
    }
    created: list[TimelineEvent] = []
    for answer in case.questionnaire_answers.all():
        if answer.question_key not in mapping:
            continue
        value = answer.answer_value_redacted.get("value")
        if value is not True:
            continue
        event_type, label = mapping[answer.question_key]
        event, was_created = TimelineEvent.objects.get_or_create(
            case=case,
            event_type=event_type,
            label=label,
            source=TimelineEvent.Source.VICTIM_STATEMENT,
            defaults={"description_redacted": f"Déclaré via questionnaire: {answer.question_key}", "confidence": answer.confidence},
        )
        if was_created:
            created.append(event)
    return created


def extract_url_indicators(text: str) -> list[ExtractedIndicator]:
    indicators: list[ExtractedIndicator] = []
    for url in sorted(set(URL_RE.findall(text or ""))):
        clean_url = url.rstrip(".,;:")
        parsed = urlparse(clean_url)
        domain = parsed.hostname or ""
        risk = "high" if any(word in clean_url.lower() for word in URGENCY_WORDS) else "medium"
        indicators.append(ExtractedIndicator("url", clean_url[:500], risk, 0.75, "URL extraite passivement, non visitée."))
        if domain:
            indicators.append(ExtractedIndicator("domain", domain[:500], risk, 0.75, "Domaine extrait depuis URL, sans résolution réseau."))
    return indicators


def extract_email_indicators_from_raw_email(raw_email_text: str) -> list[ExtractedIndicator]:
    indicators: list[ExtractedIndicator] = []
    message = Parser(policy=policy.default).parsestr(raw_email_text or "")
    for header in ("From", "Reply-To", "Return-Path"):
        value = str(message.get(header, "")).strip()
        for email_addr in EMAIL_RE.findall(value):
            indicators.append(ExtractedIndicator("email", email_addr[:500], "medium", 0.75, f"Adresse extraite du header {header}."))
    subject = str(message.get("Subject", ""))
    received = message.get_all("Received", []) or []
    for ip in IP_RE.findall("\n".join(received)):
        indicators.append(ExtractedIndicator("ip", ip, "medium", 0.6, "IP extraite d'un header Received, à relire."))
    body = raw_email_text
    indicators.extend(extract_url_indicators(body))
    if any(word in (subject + "\n" + body).lower() for word in URGENCY_WORDS):
        indicators.append(ExtractedIndicator("other", "lexique-urgence-paiement-compte", "high", 0.65, "Mots-clés d'urgence ou de paiement détectés."))
    domains = {urlparse(item.value_redacted).hostname for item in indicators if item.indicator_type == "url"}
    emails = {email.split("@")[-1].lower() for email in EMAIL_RE.findall(str(message.get("From", "")))}
    if domains and emails and not domains.intersection(emails):
        indicators.append(ExtractedIndicator("other", "mismatch-domaine-visible-reel", "high", 0.55, "Domaine d'URL différent du domaine apparent de l'expéditeur."))
    return indicators


def extract_indicators(text: str, artifact_type: str) -> list[ExtractedIndicator]:
    indicators = extract_email_indicators_from_raw_email(text) if artifact_type == EvidenceArtifact.ArtifactType.EML else extract_url_indicators(text)
    for email_addr in sorted(set(EMAIL_RE.findall(text or ""))):
        indicators.append(ExtractedIndicator("email", email_addr[:500], "medium", 0.65, "Adresse extraite du texte."))
    for phone in sorted(set(PHONE_RE.findall(text or ""))):
        indicators.append(ExtractedIndicator("phone", phone[:500], "medium", 0.65, "Téléphone extrait du texte."))
    for iban in sorted(set(IBAN_RE.findall((text or "").replace(" ", "")))):
        indicators.append(ExtractedIndicator("iban", iban[:500], "high", 0.7, "IBAN extrait du texte."))
    for ip in sorted(set(IP_RE.findall(text or ""))):
        indicators.append(ExtractedIndicator("ip", ip, "medium", 0.6, "IP extraite du texte."))
    for value in sorted(set(HASH_RE.findall(text or ""))):
        indicators.append(ExtractedIndicator("hash", value.lower(), "medium", 0.75, "Hash détecté dans le texte."))
    return indicators


def _upsert_indicator(case: ScamCase, indicator: ExtractedIndicator, artifact: EvidenceArtifact | None) -> TechnicalIndicator:
    obj, created = TechnicalIndicator.objects.get_or_create(
        case=case,
        indicator_type=indicator.indicator_type,
        value_hash=hash_value(indicator.value_redacted),
        defaults={
            "value_redacted": indicator.value_redacted,
            "source_artifact": artifact,
            "risk_level": indicator.risk_level,
            "confidence": indicator.confidence,
            "notes_redacted": indicator.notes_redacted,
        },
    )
    if created:
        _create_custody_event(case, CustodyEvent.Action.EXTRACTED_INDICATOR, artifact, {"indicator_type": indicator.indicator_type, "value_hash": obj.value_hash})
    return obj


def compute_case_risk_summary(case_id: str) -> dict[str, Any]:
    case = ScamCase.objects.get(id=case_id)
    answers = {a.question_key: a.answer_value_redacted.get("value") for a in case.questionnaire_answers.all()}
    high_flags = sum(1 for key in ("entered_password", "gave_card", "made_transfer", "installed_software", "remote_access") if answers.get(key) is True)
    lost_amount = answers.get("lost_amount") or 0
    try:
        lost_amount = float(lost_amount)
    except (TypeError, ValueError):
        lost_amount = 0
    score = min(100, high_flags * 18 + (25 if lost_amount >= 1000 else 12 if lost_amount > 0 else 0) + case.indicators.filter(risk_level="high").count() * 8)
    severity = "critical" if score >= 75 else "high" if score >= 50 else "medium" if score >= 25 else "low"
    return {"score": score, "severity": severity, "urgent_actions": recommended_actions(answers)}


def recommended_actions(answers: dict[str, Any]) -> list[str]:
    actions = ["Préserver les preuves originales et ne pas cliquer sur les liens suspects."]
    if answers.get("gave_card") or answers.get("made_transfer"):
        actions.append("Contacter immédiatement la banque, faire opposition si nécessaire et demander le rappel des fonds.")
    if answers.get("entered_password"):
        actions.append("Changer les mots de passe depuis un environnement sain et révoquer les sessions actives.")
    if answers.get("installed_software") or answers.get("remote_access"):
        actions.append("Isoler le poste victime et lancer une analyse technique défensive.")
    actions.append("Relire humainement tout rapport avant transmission à Signal Spam, 33700, 17Cyber, THESEE/PHAROS, police/gendarmerie ou banque.")
    return actions


def generate_case_reports(case_id: str) -> list[GeneratedReport]:
    case = ScamCase.objects.get(id=case_id)
    risk = compute_case_risk_summary(case_id)
    report_types = ("victim", "authorities", "bank", "company", "technical")
    reports: list[GeneratedReport] = []
    with transaction.atomic():
        for report_type in report_types:
            content = render_report(case, report_type, risk)
            report, _ = GeneratedReport.objects.update_or_create(
                case=case,
                report_type=report_type,
                defaults={"format": GeneratedReport.Format.MARKDOWN, "status": GeneratedReport.Status.DRAFT, "content_markdown": content, "sha256": compute_text_sha256(content)},
            )
            _create_custody_event(case, CustodyEvent.Action.GENERATED_REPORT, details={"report_type": report_type, "sha256": report.sha256})
            reports.append(report)
        case.severity = risk["severity"]
        case.status = ScamCase.Status.READY_FOR_REVIEW
        case.save(update_fields=["severity", "status", "updated_at"])
    return reports


def render_report(case: ScamCase, report_type: str, risk: dict[str, Any]) -> str:
    artifacts = list(case.artifacts.all())
    indicators = list(case.indicators.all())
    timeline = list(case.timeline_events.all())
    answers = list(case.questionnaire_answers.all())
    lines = [
        f"# Rapport {report_type} - Relinium Anti-Scam",
        "",
        f"- Dossier: {case.title}",
        f"- Statut: {case.status}",
        f"- Vecteur initial: {case.initial_vector}",
        f"- Score de risque: {risk['score']}/100 ({risk['severity']})",
        "",
        "## Faits prouves",
        *[f"- Artefact {a.artifact_type}: SHA-256 `{a.sha256}`, taille {a.size_bytes or 'non renseignee'} octets." for a in artifacts],
        "",
        "## Declarations victime",
        *[f"- {a.question_key}: {a.answer_value_redacted.get('value')}" for a in answers],
        "",
        "## Elements techniques",
        *[f"- {i.indicator_type}: {i.value_redacted} (risque {i.risk_level}, confiance {i.confidence:.2f})" for i in indicators[:60]],
        "",
        "## Timeline probatoire",
        *[f"- {e.occurred_at.isoformat() if e.occurred_at else 'date inconnue'} - {e.label} [{e.source}, confiance {e.confidence:.2f}]" for e in timeline],
        "",
        "## Hypotheses et correlations",
        "- Les correlations sont indicatives et doivent etre relues avant usage externe.",
        *[f"- {c.correlation_type} avec {c.target_case_id}: score {c.score:.2f}. {c.explanation}" for c in case.outgoing_correlations.all()[:20]],
        "",
        "## Actions recommandees",
        *[f"- {action}" for action in risk["urgent_actions"]],
        "",
        "## Limites",
        "- Aucun lien suspect n'a ete visite automatiquement.",
        "- Aucun rapport n'est soumis automatiquement aux autorites, banques ou plateformes.",
        "- Les champs sont minimises et doivent etre relus humainement.",
    ]
    if report_type == "bank":
        lines.insert(2, "Usage prevu: dossier banque, opposition, contestation ou rappel de fonds.")
    if report_type == "authorities":
        lines.insert(2, "Usage prevu: preparation de signalement ou plainte, apres validation humaine.")
    if report_type == "technical":
        lines.insert(2, "Usage prevu: analyse defensive interne, sans interaction agressive avec l'infrastructure suspecte.")
    if report_type == "company":
        lines.insert(2, "Usage prevu: synthese entreprise pour direction, juridique ou equipe securite.")
    return "\n".join(lines)


def correlate_case(case_id: str) -> list[CaseCorrelation]:
    case = ScamCase.objects.get(id=case_id)
    created: list[CaseCorrelation] = []
    for indicator in case.indicators.all():
        matches = TechnicalIndicator.objects.filter(indicator_type=indicator.indicator_type, value_hash=indicator.value_hash).exclude(case=case).select_related("case")
        for match in matches:
            correlation_type = {
                "domain": "shared_domain",
                "url": "shared_url_pattern",
                "phone": "shared_phone",
                "iban": "shared_iban",
                "ip": "shared_ip",
                "hash": "shared_hash",
            }.get(indicator.indicator_type, "shared_text_pattern")
            obj, was_created = CaseCorrelation.objects.get_or_create(
                source_case=case,
                target_case=match.case,
                correlation_type=correlation_type,
                defaults={"score": 0.75, "explanation": f"Indicateur partage: {indicator.indicator_type} / hash {indicator.value_hash[:12]}."},
            )
            if was_created:
                created.append(obj)
    return created


def mark_report_reviewed(report_id: str) -> GeneratedReport:
    report = GeneratedReport.objects.select_related("case").get(id=report_id)
    report.status = GeneratedReport.Status.REVIEWED
    report.reviewed_at = timezone.now()
    report.save(update_fields=["status", "reviewed_at", "generated_at"])
    _create_custody_event(report.case, CustodyEvent.Action.REVIEWED_REPORT, details={"report_type": report.report_type, "report_id": str(report.id)})
    return report
