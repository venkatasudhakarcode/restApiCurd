from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse,parse_qs
import json

from models.student_model import (
    get_student,
    add_student,
    update_student
    
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
    
    def do_PUT(self):
        path = self.path
        if path == "/updateStudentDetails":
            length = int(self.headers.get("Content-length"), 0)
            body = self.rfile(length)
            data = json.loads(body)

            student_id = data.get("id")
            name = data.get("name")

            if not student_id or not name:
                return self.send_json({"error": "id & name required"}, 400)

            updated = update_student(student_id, name)

            if updated == 0:
                return self.send_json({"error": "Student not found"}, 404)

            return self.send_json({"message": "Updated"})

        return self.send_json({"error": "Invalid route"}, 404)
    def do_DELETE(self):
        pass
        
