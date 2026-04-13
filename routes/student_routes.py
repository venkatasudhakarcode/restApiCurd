from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse,parse_qs
import json

from models.student_model import (
    get_student,
    add_student
)

class studentHandler(BaseHTTPRequestHandler):

    def send_json(self, data, status = 200):
        self.send_response(status)
        self.send_header("Content-type", "Application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        print("+++++++++++++++++++")
        
        if path == "/students":
            query = parse_qs(parsed.query)
            print(query)
            student_id = query.get("id",[None])[0]

            if student_id:
                data = get_student(student_id)
                return self.send_json(data)
            else:
                data = get_student()
                return self.send_json(data)
            
        return self.send_json({"error": "Invalid route"}, 404)
    
    def do_POST(self):

        print("+++++++++++++++++++")
        print(self.path)
        
        if self.path == "/addStudent":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)

            data = json.loads(body)
            name = data.get("name")
            age = data.get("age")

            if not name or not age:
                return self.send_json({"error": "name & age required"}, 400)

            add_student(name, age)
            return self.send_json({"message": "Student added"}, 201)

        return self.send_json({"error": "Invalid route"}, 404)
