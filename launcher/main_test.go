package main

import (
	"io"
	"net"
	"net/http"
	"net/http/httptest"
	"os"
	"path/filepath"
	"testing"
)

func TestRootRequiresExtractedGame(t *testing.T) {
	r := t.TempDir()
	if _, err := gameRoot(r); err == nil {
		t.Fatal("accepted incomplete folder")
	}
	for _, f := range []string{"index.html", "js/panorama_renderer.js", "assets/panoramic360/lobby.webp"} {
		p := filepath.Join(r, f)
		os.MkdirAll(filepath.Dir(p), 0755)
		os.WriteFile(p, []byte("local"), 0644)
	}
	if _, err := gameRoot(r); err != nil {
		t.Fatal(err)
	}
}
func TestLocalAssetsAndRange(t *testing.T) {
	r := t.TempDir()
	os.WriteFile(filepath.Join(r, "index.html"), []byte("<html>game</html>"), 0644)
	os.WriteFile(filepath.Join(r, "sound.ogg"), []byte("0123456789"), 0644)
	s := httptest.NewServer(handler(r))
	defer s.Close()
	resp, err := http.Get(s.URL + "/")
	if err != nil {
		t.Fatal(err)
	}
	defer resp.Body.Close()
	b, _ := io.ReadAll(resp.Body)
	if string(b) != "<html>game</html>" || resp.Header.Get("Cache-Control") != "no-store" {
		t.Fatal("wrong game/headers")
	}
	req, _ := http.NewRequest("GET", s.URL+"/sound.ogg", nil)
	req.Header.Set("Range", "bytes=2-4")
	res, err := http.DefaultClient.Do(req)
	if err != nil {
		t.Fatal(err)
	}
	defer res.Body.Close()
	b, _ = io.ReadAll(res.Body)
	if res.StatusCode != 206 || string(b) != "234" {
		t.Fatal("audio ranges broken")
	}
}
func TestOccupiedPortFallsBackAndStaysLoopback(t *testing.T) {
	a, err := listen(0)
	if err != nil {
		t.Fatal(err)
	}
	defer a.Close()
	port := a.Addr().(*net.TCPAddr).Port
	b, err := listen(port)
	if err != nil {
		t.Fatal(err)
	}
	defer b.Close()
	if b.Addr().(*net.TCPAddr).IP.String() != "127.0.0.1" || b.Addr().String() == a.Addr().String() {
		t.Fatal("unsafe or reused binding")
	}
}
