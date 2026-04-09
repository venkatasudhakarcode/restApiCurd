from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse, parse_qs
FILE_NAME = "students.txt"
def readStudents():
    students = []

    with open(FILE_NAME,  "r") as f:
        for line in f:
            parts = line.strip().split(',')

            student  = {
                "id":int(parts[0]),
                "name": parts[1],
                "age": int(parts[2])
            }

            students.append(student)
        
    return students

class curd(BaseHTTPRequestHandler):

    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_GET(self):

        if self.path == "/students":
            students = readStudents()
            return self.send_json(students)
        return self.send_json({"error":"invalid route"},404)
    def do_POST():
        pass

    def do_PUT():
        pass
    
    def do_DELETE():
        pass
    

server = HTTPServer(("localhost",8000),curd)
print("Server started")
server.serve_forever()

