from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse, parse_qs

studentsData = [
    {"id": 1, "name": "Venkat", "age": 36},
    {"id": 2, "name": "pandu", "age": 36},
    {"id": 3, "name": "rohi", "age": 9},
    {"id": 4, "name": "keyan", "age": 4},
    {"id": 5, "name": "prasanna", "age": 36},
    {"id": 6, "name": "jhon", "age": 55},
    {"id": 7, "name": "obama", "age": 75},
]

class students(BaseHTTPRequestHandler):

    # helper to send JSON response
    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_GET(self):
        parsedUrl = urlparse(self.path)
        path = parsedUrl.path
        query = parse_qs(parsedUrl.query)
        
        if path == "/":
            return self.send_json({"message": studentsData})

        elif path == "/students":
            studentId = query.get("id", [None])[0]

            if studentId:
                student = next(
                    (u for u in studentsData if str(u["id"]) == studentId),
                    None
                )
                if student:
                    return self.send_json({"message": student})
                else:
                    return self.send_json("Student Not Found")
            else:
                return self.send_json({"message": studentsData})

        else:
            return self.send_json({"Error": "Invalid route"}, 404)

    def do_POST(self):
        parsedUrl = urlparse(self.path)
        path = parsedUrl.path

        if path == "/addStudent":
            contentLength = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(contentLength)

            try:
                data = json.loads(body)
                name = data.get("name")

                if not name:
                    return self.send_json({"error": "Name Required"}, 400)

                newStudent = {
                    "id": len(studentsData) + 1,
                    "name": name
                }

                studentsData.append(newStudent)
                return self.send_json(studentsData, 201)

            except Exception as e:
                return self.send_json({"error": str(e)}, 400)

        else:
            return self.send_json({"Error": "Invalid route"}, 404)

    def do_PUT(self):
        parsedUrl = urlparse(self.path)
        path = parsedUrl.path

        if path == "/updateStudentDetails":
            contentLength = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(contentLength)
            print(body)
            try:
                data = json.loads(body)
                studentId = int(data.get("id"))
                print(studentId)
                name = data.get("name")
                print(name)
                if not studentId or not name:
                    return self.send_json({"error": "id and name is required"}, 400)

                student = next((u for u in studentsData if u["id"] == studentId), None)
                print(student)
                if not student:
                    return self.send_json({"error": "student Not found"}, 404)

                student["name"] = name
                return self.send_json({"message": "Student updated successfully"})

            except Exception as e:
                return self.send_json({"error": str(e)}, 400)

        else:
            return self.send_json({"Error": "Invalid route"}, 404)
        
    def do_DELETE(self):
        parsedUrl = urlparse(self.path)
        path = parsedUrl.path
        query = parse_qs(parsedUrl.query)

        if path == "/deleteStudent":
            studentId = query.get("id", [None])[0]

            if not studentId:
                return self.send_json({"Error": "Student ID required"}, 400)

            global studentsData
            studentsNewData = [u for u in studentsData if str(u["id"]) != studentId]

            if len(studentsNewData) == len(studentsData):
                return self.send_json({"error": "Student Not found"}, 404)

            studentsData = studentsNewData
            return self.send_json({"message": "Student Deleted"})

        return self.send_json({"Error": "Invalid route"}, 404)

def run(server_class=HTTPServer, handler_class=students, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}...")
    httpd.serve_forever()


if __name__ == "__main__":
    run()