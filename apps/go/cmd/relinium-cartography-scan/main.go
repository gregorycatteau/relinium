package main

import (
	"flag"
	"fmt"
	"os"
	"runtime"

	"relinium/apps/go/internal/cartography"
)

type excludesFlag []string

func (e *excludesFlag) String() string {
	return fmt.Sprint([]string(*e))
}

func (e *excludesFlag) Set(value string) error {
	*e = append(*e, value)
	return nil
}

func main() {
	var excludes excludesFlag
	config := cartography.Config{}

	flag.StringVar(&config.Root, "root", "", "root directory to scan")
	flag.StringVar(&config.Mode, "mode", "presence", "scan mode: presence or fingerprint")
	flag.StringVar(&config.Out, "out", "", "output NDJSON path")
	flag.Int64Var(&config.FingerprintBlockSize, "fingerprint-block-size", 262144, "fingerprint block size in bytes")
	flag.IntVar(&config.MaxWorkers, "max-workers", runtime.NumCPU(), "reserved for worker count compatibility")
	flag.BoolVar(&config.RedactPaths, "redact-paths", false, "redact relative paths in NDJSON output")
	flag.Var(&excludes, "exclude", "exclude pattern; may be provided multiple times")
	flag.Parse()

	config.Excludes = []string(excludes)
	scanner, err := cartography.New(config)
	if err != nil {
		fmt.Fprintln(os.Stderr, "configuration error:", err)
		os.Exit(2)
	}
	if err := scanner.Run(); err != nil {
		fmt.Fprintln(os.Stderr, "scan error:", err)
		os.Exit(1)
	}
}
