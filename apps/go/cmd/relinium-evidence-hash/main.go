package main

import (
	"crypto/sha256"
	"encoding/hex"
	"flag"
	"fmt"
	"io"
	"os"
	"path/filepath"
	"strings"
	"time"

	"relinium/apps/go/internal/ndjson"
)

const toolVersion = "relinium-evidence-hash-v0.1"

type custodyHashRecord struct {
	RecordType             string `json:"record_type"`
	ArtifactSHA256         string `json:"artifact_sha256"`
	SizeBytes              int64  `json:"size_bytes"`
	ObservedAtUTC          string `json:"observed_at_utc"`
	RelativeOrRedactedName string `json:"relative_or_redacted_name"`
	ToolVersion            string `json:"tool_version"`
}

func main() {
	var path string
	var out string
	var redactName bool
	flag.StringVar(&path, "path", "", "local artifact path to hash read-only")
	flag.StringVar(&out, "out", "", "output NDJSON path")
	flag.BoolVar(&redactName, "redact-name", false, "write only the base file name hash instead of the base name")
	flag.Parse()

	if path == "" || out == "" {
		fmt.Fprintln(os.Stderr, "usage: relinium-evidence-hash --path /chemin/preuve.eml --out artifact.ndjson")
		os.Exit(2)
	}

	sha, size, err := hashFile(path)
	if err != nil {
		fmt.Fprintln(os.Stderr, "hash error:", err)
		os.Exit(1)
	}

	name := filepath.Base(path)
	if redactName {
		sum := sha256.Sum256([]byte(name))
		name = "name_sha256:" + hex.EncodeToString(sum[:])
	}
	name = strings.TrimSpace(name)
	if name == "" || name == "." || name == string(filepath.Separator) {
		name = "artifact"
	}

	writer, err := ndjson.New(out)
	if err != nil {
		fmt.Fprintln(os.Stderr, "output error:", err)
		os.Exit(1)
	}
	defer writer.Close()

	record := custodyHashRecord{
		RecordType:             "custody_artifact_hashed",
		ArtifactSHA256:         sha,
		SizeBytes:              size,
		ObservedAtUTC:          time.Now().UTC().Format(time.RFC3339Nano),
		RelativeOrRedactedName: name,
		ToolVersion:            toolVersion,
	}
	if err := writer.Write(record); err != nil {
		fmt.Fprintln(os.Stderr, "write error:", err)
		os.Exit(1)
	}
}

func hashFile(path string) (string, int64, error) {
	info, err := os.Lstat(path)
	if err != nil {
		return "", 0, err
	}
	if !info.Mode().IsRegular() {
		return "", 0, fmt.Errorf("path is not a regular file")
	}

	file, err := os.Open(path)
	if err != nil {
		return "", 0, err
	}
	defer file.Close()

	hash := sha256.New()
	n, err := io.Copy(hash, file)
	if err != nil {
		return "", n, err
	}
	return hex.EncodeToString(hash.Sum(nil)), n, nil
}
