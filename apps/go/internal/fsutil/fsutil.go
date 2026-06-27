package fsutil

import (
	"path/filepath"
	"strings"
	"syscall"
)

func NormalizeRelative(root string, path string) (string, error) {
	rel, err := filepath.Rel(root, path)
	if err != nil {
		return "", err
	}
	if rel == "." {
		return ".", nil
	}
	rel = filepath.ToSlash(filepath.Clean(rel))
	rel = strings.TrimPrefix(rel, "./")
	return rel, nil
}

func FileType(mode uint32, modeString string) string {
	switch {
	case modeString[0] == 'd':
		return "directory"
	case modeString[0] == 'L':
		return "symlink"
	case modeString[0] == '-':
		return "file"
	default:
		_ = mode
		return "other"
	}
}

func DeviceAndInode(sys any) (*string, *uint64) {
	stat, ok := sys.(*syscall.Stat_t)
	if !ok {
		return nil, nil
	}
	device := uint64(stat.Dev)
	inode := uint64(stat.Ino)
	deviceString := strconvFormatUint(device)
	return &deviceString, &inode
}

func strconvFormatUint(value uint64) string {
	const digits = "0123456789"
	if value == 0 {
		return "0"
	}
	var buf [20]byte
	i := len(buf)
	for value > 0 {
		i--
		buf[i] = digits[value%10]
		value /= 10
	}
	return string(buf[i:])
}
