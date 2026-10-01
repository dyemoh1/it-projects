"""Loopback-only Roomly web server. Run: python server.py [--port 8001]."""
import argparse
import json
import sqlite3
from pathlib import Path
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit
from room_reservation import BookingStore

ROOT = Path(__file__).resolve().parent
ASSETS = {'/': ('reservations.html', 'text/html'), '/reservations.html': ('reservations.html', 'text/html'), '/reservations.css': ('reservations.css', 'text/css'), '/reservations.js': ('reservations.js', 'text/javascript')}

class Handler(BaseHTTPRequestHandler):
    def reply(self, status, data):
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(body)

    def trusted(self):
        allowed = {f'localhost:{self.server.server_port}', f'127.0.0.1:{self.server.server_port}'}
        host = self.headers.get('Host')
        origin = self.headers.get('Origin')
        return host in allowed and (not origin or origin == 'http://' + host)

    def do_GET(self):
        if not self.trusted():
            return self.reply(403, {'error': 'Local requests only.'})
        path = urlsplit(self.path).path
        if path == '/api/bookings':
            store = BookingStore(self.server.db_path)
            try:
                result = [dict(id=str(i), room=r, day=d, start=f'{s//60:02}:{s%60:02}', end=f'{e//60:02}:{e%60:02}', owner=o) for i,r,d,s,e,o in store.list()]
                return self.reply(200, result)
            finally:
                store.close()
        if path not in ASSETS:
            return self.reply(404, {'error': 'Not found.'})
        name, mime = ASSETS[path]
        body = (ROOT / name).read_bytes()
        self.send_response(200)
        self.send_header('Content-Type', mime + '; charset=utf-8')
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        if not self.trusted():
            return self.reply(403, {'error': 'Local requests only.'})
        if self.headers.get('Content-Type', '').split(';')[0] != 'application/json':
            return self.reply(415, {'error': 'JSON required.'})
        try:
            length = int(self.headers.get('Content-Length', '0'))
            if not 0 < length <= 4096:
                raise ValueError('Invalid request size.')
            data = json.loads(self.rfile.read(length))
            if not isinstance(data, dict):
                raise ValueError('A JSON object is required.')
            path = urlsplit(self.path).path
            fields = ('room', 'day', 'start', 'end', 'owner') if path == '/api/bookings' else ('id', 'owner')
            if path not in ('/api/bookings', '/api/cancel'):
                return self.reply(404, {'error': 'Not found.'})
            if any(not isinstance(data.get(k), str) or not data[k].strip() or len(data[k]) > 80 for k in fields):
                raise ValueError('Required fields must be nonempty text of at most 80 characters.')
            store = BookingStore(self.server.db_path)
            try:
                if path == '/api/bookings':
                    bid = store.reserve(**{k:data[k] for k in fields})
                    return self.reply(201, {'id': str(bid)})
                store.cancel(int(data['id']), data['owner'])
                return self.reply(200, {'ok': True})
            finally:
                store.close()
        except (ValueError, UnicodeError) as error:
            return self.reply(409 if 'overlaps' in str(error) else 400, {'error': str(error)})
        except sqlite3.Error:
            return self.reply(503, {'error': 'Database unavailable. Try again.'})


def make_server(port=8001, db_path=None):
    server = ThreadingHTTPServer(('127.0.0.1', port), Handler)
    server.db_path = str(db_path or ROOT / 'bookings.db')
    return server

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=8001)
    parser.add_argument('--db', default=str(ROOT / 'bookings.db'))
    args = parser.parse_args()
    server = make_server(args.port, args.db)
    print(f'Roomly: http://localhost:{server.server_port}', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
