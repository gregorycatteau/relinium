package evidence

type SnapshotStarted struct {
	EventType          string   `json:"event_type"`
	SnapshotID         string   `json:"snapshot_id"`
	StartedAtUTC       string   `json:"started_at_utc"`
	ScannerVersion     string   `json:"scanner_version"`
	Mode               string   `json:"mode"`
	RootID             string   `json:"root_id"`
	RootRefHash        string   `json:"root_ref_hash"`
	NormalizationRules []string `json:"normalization_rules"`
}

type Observation struct {
	EventType              string  `json:"event_type"`
	SnapshotID             string  `json:"snapshot_id"`
	RelativePath           string  `json:"relative_path"`
	PathHash               string  `json:"path_hash"`
	FileType               string  `json:"file_type"`
	Size                   int64   `json:"size"`
	MtimeUTC               string  `json:"mtime_utc"`
	Permissions            string  `json:"permissions"`
	DeviceIDHash           *string `json:"device_id_hash"`
	Inode                  *uint64 `json:"inode"`
	MetadataHash           string  `json:"metadata_hash"`
	LocationHash           string  `json:"location_hash"`
	FingerprintHash        *string `json:"fingerprint_hash"`
	ContentHash            *string `json:"content_hash"`
	ObservationHash        string  `json:"observation_hash"`
	ObservedAtUTC          string  `json:"observed_at_utc"`
	ObservationStartedUTC  string  `json:"observation_started_at_utc"`
	ObservationFinishedUTC string  `json:"observation_finished_at_utc"`
	ErrorCode              *string `json:"error_code"`
}

type ScanError struct {
	EventType     string `json:"event_type"`
	SnapshotID    string `json:"snapshot_id"`
	RelativePath  string `json:"relative_path"`
	PathHash      string `json:"path_hash"`
	ErrorCode     string `json:"error_code"`
	ErrorMessage  string `json:"error_message_redacted"`
	ObservedAtUTC string `json:"observed_at_utc"`
}

type SnapshotSealed struct {
	EventType        string `json:"event_type"`
	SnapshotID       string `json:"snapshot_id"`
	StartedAtUTC     string `json:"started_at_utc"`
	FinishedAtUTC    string `json:"finished_at_utc"`
	DurationMS       int64  `json:"duration_ms"`
	ScannerVersion   string `json:"scanner_version"`
	ObservationCount int    `json:"observation_count"`
	ErrorCount       int    `json:"error_count"`
	SnapshotHash     string `json:"snapshot_hash"`
}
