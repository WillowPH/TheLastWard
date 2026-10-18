# Native Windows launcher

START_GAME.exe is a Windows x64 console executable built from this directory using
Go's standard library with CGO disabled. It runs a local file server bound to
127.0.0.1 and opens the default browser. No Python, Node, installer, remote artwork
service or internet connection is needed. All game files remain separate.

Extract the entire project ZIP. Keep the EXE next to index.html. Keep its console
window open while playing. If the preferred port 8123 is busy, an available local
port is used. Saves belong to the browser/address; keep the same port for continuing.
`--no-browser`, `--port` and `--root` are available for diagnostics.

Rebuild with Go 1.27.2 (or a compatible later toolchain):

```
GO111MODULE=off go test ./launcher
GO111MODULE=off CGO_ENABLED=0 GOOS=windows GOARCH=amd64 go build -trimpath -ldflags="-s -w" -o START_GAME.exe ./launcher
```

The release is not code-signed. The automated server tests run on Linux from the
same source; opening a Windows desktop browser has not been tested on Windows here.
