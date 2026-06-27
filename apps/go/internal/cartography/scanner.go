package cartography

import (
	"crypto/rand"
	"encoding/hex"
	"errors"
	"fmt"
	"io/fs"
	"os"
	"path/filepath"
	"runtime"
	"strings"
	"sync"
	"time"

	"relinium/apps/go/internal/evidence"
	"relinium/apps/go/internal/fsutil"
	"relinium/apps/go/internal/hashing"
	"relinium/apps/go/internal/ndjson"
	"relinium/apps/go/internal/seal"
)

const ScannerVersion = "relinium-cartography-scan/0.1.0"

type Config struct {
	Root                 string
	Mode                 string
	Out                  string
	FingerprintBlockSize int64
	MaxWorkers           int
	Excludes             []string
	RedactPaths          bool
}

type Scanner struct {
	config Config
}

type scanTask struct {
	path string
	rel  string
}

type scanResult struct {
	observation *evidence.Observation
	scanError   *evidence.ScanError
}

func New(config Config) (*Scanner, error) {
	if config.Root == "" {
		return nil, errors.New("--root is required")
	}
	if config.Out == "" {
		return nil, errors.New("--out is required")
	}
	if config.Mode == "" {
		config.Mode = "presence"
	}
	if config.Mode != "presence" && config.Mode != "fingerprint" {
		return nil, fmt.Errorf("unsupported mode %q", config.Mode)
	}
	if config.FingerprintBlockSize <= 0 {
		config.FingerprintBlockSize = 262144
	}
	if config.MaxWorkers <= 0 {
		config.MaxWorkers = runtime.NumCPU()
	}
	return &Scanner{config: config}, nil
}

func (s *Scanner) Run() error {
	root, err := filepath.Abs(s.config.Root)
	if err != nil {
		return err
	}
	root = filepath.Clean(root)

	writer, err := ndjson.New(s.config.Out)
	if err != nil {
		return err
	}
	defer writer.Close()

	snapshotID := randomID()
	rootID := hashing.String("root:" + snapshotID)
	rootRefHash := hashing.String(root)
	start := time.Now()
	startUTC := start.UTC().Format(time.RFC3339Nano)

	err = writer.Write(evidence.SnapshotStarted{
		EventType:      "snapshot_started",
		SnapshotID:     snapshotID,
		StartedAtUTC:   startUTC,
		ScannerVersion: ScannerVersion,
		Mode:           s.config.Mode,
		RootID:         rootID,
		RootRefHash:    rootRefHash,
		NormalizationRules: []string{
			"relative-path",
			"filepath-clean",
			"slash-separators",
			"no-symlink-follow",
		},
	})
	if err != nil {
		return err
	}

	tasks := make(chan scanTask)
	results := make(chan scanResult)
	walkErrs := make(chan error, 1)

	var workers sync.WaitGroup
	for i := 0; i < s.config.MaxWorkers; i++ {
		workers.Add(1)
		go func() {
			defer workers.Done()
			for task := range tasks {
				info, err := os.Lstat(task.path)
				if err != nil {
					scanError := s.scanError(snapshotID, rootID, task.rel, "stat_error", err)
					results <- scanResult{scanError: &scanError}
					continue
				}
				obs, err := s.observe(snapshotID, rootID, root, task.path, task.rel, info)
				if err != nil {
					scanError := s.scanError(snapshotID, rootID, task.rel, "observation_error", err)
					results <- scanResult{scanError: &scanError}
					continue
				}
				results <- scanResult{observation: &obs}
			}
		}()
	}

	go func() {
		walkErr := filepath.WalkDir(root, func(path string, entry fs.DirEntry, walkErr error) error {
			rel, relErr := fsutil.NormalizeRelative(root, path)
			if relErr != nil {
				rel = "unknown"
			}
			if rel != "." && s.excluded(rel) {
				if entry != nil && entry.IsDir() {
					return filepath.SkipDir
				}
				return nil
			}
			if walkErr != nil {
				scanError := s.scanError(snapshotID, rootID, rel, "walk_error", walkErr)
				results <- scanResult{scanError: &scanError}
				return nil
			}
			tasks <- scanTask{path: path, rel: rel}
			return nil
		})
		close(tasks)
		workers.Wait()
		close(results)
		walkErrs <- walkErr
	}()

	var observationHashes []string
	errorCount := 0
	observationCount := 0
	for result := range results {
		if result.scanError != nil {
			errorCount++
			if err := writer.Write(*result.scanError); err != nil {
				return err
			}
			continue
		}
		if result.observation != nil {
			observationCount++
			observationHashes = append(observationHashes, result.observation.ObservationHash)
			if err := writer.Write(*result.observation); err != nil {
				return err
			}
		}
	}
	if walkErr := <-walkErrs; walkErr != nil {
		errorCount++
	}

	finished := time.Now()
	return writer.Write(evidence.SnapshotSealed{
		EventType:        "snapshot_sealed",
		SnapshotID:       snapshotID,
		StartedAtUTC:     startUTC,
		FinishedAtUTC:    finished.UTC().Format(time.RFC3339Nano),
		DurationMS:       finished.Sub(start).Milliseconds(),
		ScannerVersion:   ScannerVersion,
		ObservationCount: observationCount,
		ErrorCount:       errorCount,
		SnapshotHash:     seal.SnapshotHash(observationHashes),
	})
}

func (s *Scanner) observe(snapshotID string, rootID string, root string, path string, rel string, info fs.FileInfo) (evidence.Observation, error) {
	started := time.Now().UTC()
	visibleRel := rel
	if s.config.RedactPaths {
		visibleRel = "redacted"
	}
	mode := info.Mode()
	fileType := "other"
	switch {
	case mode.IsRegular():
		fileType = "file"
	case mode.IsDir():
		fileType = "directory"
	case mode&fs.ModeSymlink != 0:
		fileType = "symlink"
	}

	deviceID, inode := fsutil.DeviceAndInode(info.Sys())
	var deviceIDHash *string
	if deviceID != nil {
		value := hashing.String(*deviceID)
		deviceIDHash = &value
	}

	locationPayload := map[string]any{
		"root_id":               rootID,
		"relative_path":         rel,
		"normalization_version": "relinium-path-v1",
	}
	locationHash, err := hashing.CanonicalJSON(locationPayload)
	if err != nil {
		return evidence.Observation{}, err
	}
	pathHash := locationHash

	metadataPayload := map[string]any{
		"file_type":      fileType,
		"size":           info.Size(),
		"mtime_utc":      info.ModTime().UTC().Format(time.RFC3339Nano),
		"permissions":    mode.Perm().String(),
		"device_id_hash": deviceIDHash,
		"inode":          inode,
	}
	metadataHash, err := hashing.CanonicalJSON(metadataPayload)
	if err != nil {
		return evidence.Observation{}, err
	}

	var fingerprintHash *string
	if s.config.Mode == "fingerprint" && mode.IsRegular() {
		value, err := hashing.FileBlocks(path, info.Size(), s.config.FingerprintBlockSize)
		if err != nil {
			return evidence.Observation{}, err
		}
		fingerprintHash = value
	}

	finished := time.Now().UTC()
	observationPayload := map[string]any{
		"root_id":                     rootID,
		"relative_path":               rel,
		"file_type":                   fileType,
		"size":                        info.Size(),
		"mtime_utc":                   info.ModTime().UTC().Format(time.RFC3339Nano),
		"permissions":                 mode.Perm().String(),
		"metadata_hash":               metadataHash,
		"location_hash":               locationHash,
		"fingerprint_hash":            fingerprintHash,
		"content_hash":                nil,
		"scanner_version":             ScannerVersion,
		"observation_started_at_utc":  started.Format(time.RFC3339Nano),
		"observation_finished_at_utc": finished.Format(time.RFC3339Nano),
		"error_code":                  nil,
	}
	observationHash, err := hashing.CanonicalJSON(observationPayload)
	if err != nil {
		return evidence.Observation{}, err
	}

	return evidence.Observation{
		EventType:              "observation",
		SnapshotID:             snapshotID,
		RelativePath:           visibleRel,
		PathHash:               pathHash,
		FileType:               fileType,
		Size:                   info.Size(),
		MtimeUTC:               info.ModTime().UTC().Format(time.RFC3339Nano),
		Permissions:            mode.Perm().String(),
		DeviceIDHash:           deviceIDHash,
		Inode:                  inode,
		MetadataHash:           metadataHash,
		LocationHash:           locationHash,
		FingerprintHash:        fingerprintHash,
		ContentHash:            nil,
		ObservationHash:        observationHash,
		ObservedAtUTC:          finished.Format(time.RFC3339Nano),
		ObservationStartedUTC:  started.Format(time.RFC3339Nano),
		ObservationFinishedUTC: finished.Format(time.RFC3339Nano),
		ErrorCode:              nil,
	}, nil
}

func (s *Scanner) scanError(snapshotID string, rootID string, rel string, code string, err error) evidence.ScanError {
	visibleRel := rel
	if s.config.RedactPaths {
		visibleRel = "redacted"
	}
	locationHash, _ := hashing.CanonicalJSON(map[string]any{
		"root_id":               rootID,
		"relative_path":         rel,
		"normalization_version": "relinium-path-v1",
	})
	return evidence.ScanError{
		EventType:     "scan_error",
		SnapshotID:    snapshotID,
		RelativePath:  visibleRel,
		PathHash:      locationHash,
		ErrorCode:     code,
		ErrorMessage:  redactError(err),
		ObservedAtUTC: time.Now().UTC().Format(time.RFC3339Nano),
	}
}

func (s *Scanner) excluded(rel string) bool {
	for _, pattern := range s.config.Excludes {
		if pattern == "" {
			continue
		}
		matched, _ := filepath.Match(pattern, rel)
		if matched {
			return true
		}
		matched, _ = filepath.Match(pattern, filepath.Base(rel))
		if matched {
			return true
		}
		if strings.HasPrefix(rel, strings.TrimSuffix(pattern, "/")+"/") {
			return true
		}
	}
	return false
}

func redactError(err error) string {
	if err == nil {
		return ""
	}
	value := err.Error()
	if len(value) > 240 {
		value = value[:240]
	}
	return value
}

func randomID() string {
	var buf [16]byte
	_, err := rand.Read(buf[:])
	if err != nil {
		return hashing.String(time.Now().UTC().Format(time.RFC3339Nano))[:32]
	}
	return hex.EncodeToString(buf[:])
}
