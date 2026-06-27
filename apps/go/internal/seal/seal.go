package seal

import (
	"sort"
	"strings"

	"relinium/apps/go/internal/hashing"
)

func SnapshotHash(observationHashes []string) string {
	values := append([]string(nil), observationHashes...)
	sort.Strings(values)
	return hashing.String(strings.Join(values, "\n"))
}
