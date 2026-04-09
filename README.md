# restApiCurd

You created a server using:

BaseHTTPRequestHandler → handles HTTP requests
HTTPServer → runs server on port 8000

Endpoints you built:

Method	URL	Purpose
GET	/students	Get all or one student
POST	/addStudent	Add new student
PUT	/updateStudentDetails	Update student
DELETE	/deleteStudent?id=1	Delete student

Curl Urls :

GET all
curl http://localhost:8000/students

GET by ID
curl "http://localhost:8000/students?id=5"

POST
curl -X POST http://localhost:8000/addStudent \
-H "Content-Type: application/json" \
-d "{\"name\":\"sudhakar\"}"

PUT 
curl -X PUT http://localhost:8000/updateStudentDetails \
-H "Content-Type: application/json" \
-d "{\"id\":5,\"name\":\"sudhakar\"}"

DELETE
curl -X DELETE "http://localhost:8000/deleteStudent?id=5"


