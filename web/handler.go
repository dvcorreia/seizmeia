package web

import (
	"embed"
	"errors"
	"io"
	"mime"
	"net/http"
	"path"
	"path/filepath"
)

//go:generate npm run build -w app

// dist containing the static web content.
//
//go:embed app/dist/*
var dist embed.FS

var ErrDir = errors.New("path is dir")

func tryRead(fs embed.FS, prefix, requestedPath string, w http.ResponseWriter) error {
	f, err := fs.Open(path.Join(prefix, requestedPath))
	if err != nil {
		return err
	}
	defer f.Close()

	stat, _ := f.Stat()
	if stat.IsDir() {
		return ErrDir
	}

	contentType := mime.TypeByExtension(filepath.Ext(requestedPath))
	w.Header().Set("Content-Type", contentType)
	_, err = io.Copy(w, f)
	return err
}

func SPAHandler(w http.ResponseWriter, r *http.Request) {
	err := tryRead(dist, "app/dist", r.URL.Path, w)
	if err == nil {
		return
	}
	err = tryRead(dist, "app/dist", "index.html", w)
	if err != nil {
		panic(err)
	}
}
