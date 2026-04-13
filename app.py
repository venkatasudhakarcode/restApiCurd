from http.server import HTTPServer
from routes.student_routes import studentHandler

def run():
    server = HTTPServer(("", 8080), studentHandler)
    print("Server running on port 8000...")
    server.serve_forever()

if __name__ == "__main__":
    run()