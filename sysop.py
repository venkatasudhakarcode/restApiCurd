import os
import sys
import json
from urllib.parse import urlparse, parse_qs
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000

# In-memory DB
users = [
    {"id": 1, "name": "Sudhakar"},
    {"id": 2, "name": "Venkat"}
]

class MyHandler(BaseHTTPRequestHandler):

    # Helper to send JSON response
    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    # GET API
    def do_GET(self):
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        query = parse_qs(parsed_url.query)

        # Example: /users?id=1
        if path == "/users":
            user_id = query.get("id", [None])[0]

            if user_id:
                user = next((u for u in users if str(u["id"]) == user_id), None)
                if user:
                    return self.send_json(user)
                else:
                    return self.send_json({"error": "User not found"}, 404)

            return self.send_json(users)

        # Example: /external
        elif path == "/external":
            r = requests.get("https://api.github.com")
            return self.send_json({
                "status": r.status_code,
                "headers": dict(r.headers)
            })

        # Example: /
        elif path == "/":
            return self.send_json({
                "message": "Server running",
                "cwd": os.getcwd()
            })

        else:
            return self.send_json({"error": "Invalid route"}, 404)

    # POST API
    def do_POST(self):
        parsed_url = urlparse(self.path)

        if parsed_url.path == "/users":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)

            try:
                data = json.loads(body)
                name = data.get("name")

                if not name:
                    return self.send_json({"error": "Name required"}, 400)

                new_user = {
                    "id": len(users) + 1,
                    "name": name
                }
                users.append(new_user)

                return self.send_json(new_user, 201)

            except Exception as e:
                return self.send_json({"error": str(e)}, 400)

        else:
            return self.send_json({"error": "Invalid route"}, 404)


# Start server
server = HTTPServer(("localhost", PORT), MyHandler)
print(f"🚀 Server running on http://localhost:{PORT}")

server.serve_forever()