import http.server, socketserver
import hashlib
import random
import subprocess

listen_port = 30401

class my_handler(http.server.BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.end_headers()
        self.send_response(200)
    def do_GET(self):
        self.send_response(200)
        if self.path.startswith('/trigger'):
            self.send_header("Content-type", "text/plain; charset=utf-8")
            self.end_headers()
            with open('/tmp/trigger', 'w+') as f:
                f.write(str(random.random()))
            self.wfile.write('ok'.encode('utf-8'))
            return
        self.send_response(403)
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write('invalid get query.'.encode('utf-8'))


try:
    server = http.server.HTTPServer(('', listen_port), my_handler)
    print('Listening *:' + str(listen_port))
    server.serve_forever()
except KeyboardInterrupt:
    server.socket.close()

