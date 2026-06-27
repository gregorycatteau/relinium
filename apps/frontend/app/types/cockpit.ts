export type StatusValue = 'pass' | 'failed' | 'ok' | string

export interface Summary {
  ssot_root: string
  baseline_path: string
  validator_path: string
  validation: {
    strict_status: StatusValue
    with_baseline_status: StatusValue
    strict_finding_count: number
    known_finding_count: number
    matched_baseline_count: number
  }
  counts: {
    streams: number
    events: number
    documents: number
  }
  roadmap: Array<{
    label: string
    progress: number
    status: string
  }>
}

export interface EventStream {
  path: string
  tenant: string
  event_count: number
  kinds: Record<string, number>
  last_event?: EventRecord | null
}

export interface Finding {
  severity: string
  location: string
  code: string
  message: string
  stream_path?: string
  line_number?: number
  event_id?: string
  raw_line_sha256?: string
  formatted?: string
}

export interface EventRecord {
  id: string
  kind: string
  event_type: string
  timestamp: string
  tenant_id: string
  actor_human: string
  actor_agent: string
  path?: string
  hash_sha256?: string
  genesis?: boolean
  comment?: string
  line: number
  stream_path: string
  raw_line_sha256: string
  validation?: {
    status: 'hash_ok' | 'baseline' | 'anomaly' | 'unchecked'
    actual_hash?: string
    finding?: Finding
    known_finding?: unknown
  }
}

export interface DocumentRecord {
  path: string
  exists: boolean
  declared_hash?: string
  actual_hash?: string
  hash_status: 'ok' | 'anomaly' | string
  referenced_by?: string
  event_line?: number
  stream_path?: string
}

export interface EventsPayload {
  count: number
  events: EventRecord[]
  documents: DocumentRecord[]
}

export interface ValidationPayload {
  strict: {
    status: StatusValue
    finding_count: number
    findings: Finding[]
  }
  with_baseline: {
    status: StatusValue
    finding_count: number
    matched_baseline_count: number
    findings: Finding[]
  }
  known_findings: {
    path: string
    count: number
    findings: unknown[]
  }
}
