from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        response = {
            "service": "backend",
            "status": "healthy"
        }

        body = json.dumps(response).encode()

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

server = HTTPServer(("0.0.0.0", 8000), Handler)
print("Backend listening on port 8000")
server.serve_forever()
