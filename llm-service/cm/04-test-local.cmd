@echo off
curl -X POST "http://127.0.0.1:8081/llm/embed" ^
     -H "Content-Type: application/json" ^
     -d "{\"text\": \"Bluetooth Headset\"}"
rem  curl -X GET "http://127.0.0.1:8081/llm/health"
@echo on
