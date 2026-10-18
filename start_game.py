"""Launch the extracted multi-file game locally; no packages or internet required."""
from functools import partial
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
import argparse,threading,webbrowser
ROOT=Path(__file__).resolve().parent
class Handler(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
 def end_headers(self):
  self.send_header('Cache-Control','no-cache')
  super().end_headers()
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--port',type=int,default=8123);parser.add_argument('--no-browser',action='store_true');args=parser.parse_args()
 try:server=ThreadingHTTPServer(('127.0.0.1',args.port),partial(Handler,directory=str(ROOT)))
 except OSError:server=ThreadingHTTPServer(('127.0.0.1',0),partial(Handler,directory=str(ROOT)))
 url='http://127.0.0.1:'+str(server.server_port)+'/'
 print('THE LAST WARD — Chapter 1\n'+url+'\nKeep this window open while playing. Press Ctrl+C to stop.',flush=True)
 if not args.no_browser:threading.Timer(.3,lambda:webbrowser.open(url)).start()
 try:server.serve_forever()
 except KeyboardInterrupt:pass
 finally:server.server_close()
if __name__=='__main__':main()
