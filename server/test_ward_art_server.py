"""Local-only gateway regressions: python -m unittest discover -s server -v."""
import base64
import concurrent.futures
import importlib.util
import json
import pathlib
import shutil
import struct
import tempfile
import threading
import time
import unittest
import urllib.error
import urllib.request
import zlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from unittest import mock


def png_image():
    def chunk(kind, data):
        return struct.pack('!I', len(data)) + kind + data + struct.pack('!I', zlib.crc32(kind + data))
    pixels = b''.join(b'\0' + b''.join(bytes((x, y, (x + y) % 256)) for x in range(64)) for y in range(64))
    return (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('!2I5B', 64, 64, 8, 2, 0, 0, 0))
            + chunk(b'IDAT', zlib.compress(pixels)) + chunk(b'IEND', b''))


IMAGE = png_image()


class MockGateway(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def do_POST(self):
        with self.server.calls_lock:
            self.server.calls += 1
            self.server.authorization = self.headers.get('Authorization')
            self.server.payload = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
        time.sleep(0.1)  # Make simultaneous cache misses overlap deterministically.
        mode = self.server.mode
        if mode == 'error':
            self.send_error(503, 'mock provider unavailable')
            return
        body = {'image_base64': base64.b64encode(IMAGE).decode()}
        if mode == 'invalid_image':
            body = {'image_base64': base64.b64encode(b'x' * 200).decode()}
        elif mode == 'insecure_url':
            body = {'image_url': 'http://127.0.0.1/never-fetch-this'}
        data = json.dumps(body).encode()
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)


class ArtServerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='ward-art-test-')
        self.addCleanup(self.temp.cleanup)
        root = pathlib.Path(self.temp.name)
        (root / 'server').mkdir()
        (root / 'assets' / 'rooms').mkdir(parents=True)
        (root / 'assets' / 'rooms' / 'test_room.webp').touch()
        source = pathlib.Path(__file__).with_name('ward_art_server.py')
        copied = root / 'server' / source.name
        shutil.copyfile(source, copied)
        spec = importlib.util.spec_from_file_location('ward_art_test_target', copied)
        self.art = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.art)
        self.art.UPSTREAM = ''
        self.art.KEY = 'local-test-secret'

        class QuietHandler(self.art.Handler):
            def log_message(self, *args):
                pass

        self.site = self.start_server(QuietHandler)
        self.base = 'http://127.0.0.1:' + str(self.site.server_port)
        self.gateway = self.start_server(MockGateway)
        self.gateway.calls = 0
        self.gateway.calls_lock = threading.Lock()
        self.gateway.mode = 'success'

    def start_server(self, handler):
        server = ThreadingHTTPServer(('127.0.0.1', 0), handler)
        worker = threading.Thread(target=server.serve_forever, daemon=True)
        worker.start()
        self.addCleanup(server.server_close)
        self.addCleanup(worker.join)
        self.addCleanup(server.shutdown)
        return server

    def enable_provider(self):
        self.art.UPSTREAM = 'http://127.0.0.1:' + str(self.gateway.server_port) + '/generate'

    def request_json(self, path='/api/ward-art', payload=None):
        data = json.dumps(payload).encode() if payload is not None else None
        request = urllib.request.Request(self.base + path, data=data, headers={'Content-Type': 'application/json'})
        try:
            response = urllib.request.urlopen(request, timeout=5)
        except urllib.error.HTTPError as error:
            response = error
        with response:
            return response.status, json.load(response)

    def test_capability_metadata_and_unconfigured_fallback(self):
        self.assertEqual(self.request_json('/data/art_service.json'), (200, {'available': False, 'endpoint': None}))
        status, body = self.request_json(payload={'room': 'test_room', 'seed': 'test'})
        self.assertEqual(status, 503)
        self.assertIn('bundled room artwork', body['error'])
        self.assertEqual(self.gateway.calls, 0)
        self.enable_provider()
        self.assertEqual(self.request_json('/data/art_service.json'), (200, {'available': True, 'endpoint': '/api/ward-art'}))

    def test_concurrent_requests_publish_once_and_reuse_cache(self):
        self.enable_provider()
        barrier = threading.Barrier(2)
        payload = {'room': 'test_room', 'seed': 'shared_seed', 'powered': False}

        def request():
            barrier.wait(timeout=5)
            return self.request_json(payload=payload)

        original_replace = self.art.os.replace
        publications = []

        def publish_complete(source, destination):
            self.assertFalse(destination.exists())
            self.assertEqual(source.read_bytes(), IMAGE)
            publications.append(destination)
            original_replace(source, destination)

        with mock.patch.object(self.art.os, 'replace', side_effect=publish_complete):
            with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
                replies = list(pool.map(lambda _: request(), range(2)))
        self.assertEqual([status for status, _ in replies], [200, 200])
        self.assertEqual(replies[0], replies[1])
        self.assertEqual(self.gateway.calls, 1)
        self.assertEqual(self.gateway.authorization, 'Bearer local-test-secret')
        self.assertEqual(len(publications), 1)
        self.assertEqual(list(self.art.GENERATED.iterdir()), publications)
        with urllib.request.urlopen(replies[0][1]['image_url'], timeout=5) as response:
            self.assertEqual(response.read(), IMAGE)
        self.assertEqual(self.request_json(payload=payload), replies[0])
        self.assertEqual(self.gateway.calls, 1)

    def test_provider_errors_keep_cache_empty_and_credentials_private(self):
        self.enable_provider()
        for mode in ('error', 'invalid_image', 'insecure_url'):
            with self.subTest(mode=mode):
                self.gateway.mode = mode
                status, body = self.request_json(payload={'room': 'test_room', 'seed': mode})
                self.assertEqual(status, 502)
                self.assertEqual(body, {'error': 'Image service error; local artwork still works.'})
                self.assertNotIn(self.art.KEY, json.dumps(body))
                self.assertEqual(list(self.art.GENERATED.iterdir()), [])

    def test_failed_publication_removes_temporary_file(self):
        target = self.art.GENERATED / 'image.png'
        with mock.patch.object(self.art.os, 'replace', side_effect=OSError('disk unavailable')):
            with self.assertRaises(OSError):
                self.art._publish_image(target, IMAGE)
        self.assertEqual(list(self.art.GENERATED.iterdir()), [])


if __name__ == '__main__':
    unittest.main()
