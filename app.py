from http.server import HTTPServer
from routes.student_routes import studentHandler

def run():
    server = HTTPServer(("", 9090), studentHandler)
    print("Server running on port 9090...")
    server.serve_forever()

if __name__ == "__main__":
    run()