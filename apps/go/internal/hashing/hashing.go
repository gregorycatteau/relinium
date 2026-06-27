package hashing

import (
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"io"
	"os"
)

func Bytes(data []byte) string {
	sum := sha256.Sum256(data)
	return hex.EncodeToString(sum[:])
}

func String(value string) string {
	return Bytes([]byte(value))
}

func CanonicalJSON(value any) (string, error) {
	data, err := json.Marshal(value)
	if err != nil {
		return "", err
	}
	return Bytes(data), nil
}

func FileBlocks(path string, size int64, blockSize int64) (*string, error) {
	if size < 0 {
		size = 0
	}
	if blockSize <= 0 {
		blockSize = 262144
	}

	file, err := os.Open(path)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	firstHash, firstBytes, err := readBlockAt(file, 0, minInt64(blockSize, size))
	if err != nil {
		return nil, err
	}

	lastOffset := int64(0)
	if size > blockSize {
		lastOffset = size - blockSize
	}
	lastHash, lastBytes, err := readBlockAt(file, lastOffset, minInt64(blockSize, size-lastOffset))
	if err != nil {
		return nil, err
	}

	payload := map[string]any{
		"strategy":    "first-last-sha256-v1",
		"size":        size,
		"block_size":  blockSize,
		"first_hash":  firstHash,
		"first_bytes": firstBytes,
		"last_hash":   lastHash,
		"last_bytes":  lastBytes,
		"last_offset": lastOffset,
	}
	value, err := CanonicalJSON(payload)
	if err != nil {
		return nil, err
	}
	return &value, nil
}

func readBlockAt(file *os.File, offset int64, length int64) (string, int64, error) {
	if length <= 0 {
		return String(""), 0, nil
	}
	_, err := file.Seek(offset, io.SeekStart)
	if err != nil {
		return "", 0, err
	}
	buf := make([]byte, length)
	n, err := io.ReadFull(file, buf)
	if err != nil && err != io.ErrUnexpectedEOF && err != io.EOF {
		return "", int64(n), err
	}
	return Bytes(buf[:n]), int64(n), nil
}

func minInt64(a int64, b int64) int64 {
	if a < b {
		return a
	}
	return b
}
