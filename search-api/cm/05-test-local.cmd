@echo off
curl -X GET "http://127.0.0.1:8080/search/actuator/health"
curl -X POST "http://127.0.0.1:8080/search/search" ^
     -H "Content-Type: application/json" ^
     -d "{\"query\": \"Bluetooth Headset\", \"limit\": 10}"
@echo on