package ndjson

import (
	"encoding/json"
	"os"
)

type Writer struct {
	file *os.File
	enc  *json.Encoder
}

func New(path string) (*Writer, error) {
	file, err := os.Create(path)
	if err != nil {
		return nil, err
	}
	return &Writer{file: file, enc: json.NewEncoder(file)}, nil
}

func (w *Writer) Write(value any) error {
	return w.enc.Encode(value)
}

func (w *Writer) Close() error {
	return w.file.Close()
}
