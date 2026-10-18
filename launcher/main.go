// The Last Ward local launcher. Go standard library only; CGO disabled in release.
package main

import (
	"flag"
	"fmt"
	"net"
	"net/http"
	"os"
	"os/exec"
	"path/filepath"
	"runtime"
	"time"
)

func gameRoot(override string) (string, error) {
	root := override
	if root == "" {
		executable, err := os.Executable()
		if err != nil {
			return "", err
		}
		root = filepath.Dir(executable)
	}
	root, err := filepath.Abs(root)
	if err != nil {
		return "", err
	}
	for _, name := range []string{"index.html", "js/panorama_renderer.js", "assets/panoramic360/lobby.webp"} {
		info, err := os.Stat(filepath.Join(root, filepath.FromSlash(name)))
		if err != nil || info.IsDir() {
			return "", fmt.Errorf("missing %s: extract the WHOLE project ZIP first, then run START_GAME.exe from that folder", name)
		}
	}
	return root, nil
}
func handler(root string) http.Handler {
	files := http.FileServer(http.Dir(root))
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		// Serve locally only, without stale artwork/scripts or third-party services.
		w.Header().Set("Cache-Control", "no-store")
		w.Header().Set("X-Content-Type-Options", "nosniff")
		files.ServeHTTP(w, r)
	})
}
func listen(port int) (net.Listener, error) {
	l, err := net.Listen("tcp4", fmt.Sprintf("127.0.0.1:%d", port))
	if err != nil && port != 0 {
		return net.Listen("tcp4", "127.0.0.1:0")
	}
	return l, err
}
func openBrowser(url string) error {
	switch runtime.GOOS {
	case "windows":
		return exec.Command("rundll32.exe", "url.dll,FileProtocolHandler", url).Start()
	case "darwin":
		return exec.Command("open", url).Start()
	default:
		return exec.Command("xdg-open", url).Start()
	}
}
func run() error {
	rootFlag := flag.String("root", "", "project folder (defaults to the launcher's folder)")
	port := flag.Int("port", 8123, "local port (an available port is used if busy)")
	noBrowser := flag.Bool("no-browser", false, "print the address without opening a browser")
	flag.Parse()
	root, err := gameRoot(*rootFlag)
	if err != nil {
		return err
	}
	l, err := listen(*port)
	if err != nil {
		return err
	}
	defer l.Close()
	url := "http://" + l.Addr().String() + "/"
	fmt.Println("THE LAST WARD - Chapter 1\n" + url + "\nKeep this window open while playing. Close it to stop the game.\nPython and internet access are NOT required.")
	if !*noBrowser {
		go func() {
			time.Sleep(300 * time.Millisecond)
			if err := openBrowser(url); err != nil {
				fmt.Println("Open this address in your browser:", url)
			}
		}()
	}
	return (&http.Server{Handler: handler(root), ReadHeaderTimeout: 10 * time.Second}).Serve(l)
}
func main() {
	if err := run(); err != nil {
		fmt.Fprintln(os.Stderr, "Could not start The Last Ward:", err)
		os.Exit(1)
	}
}
