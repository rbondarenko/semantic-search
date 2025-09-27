curl -X POST "http://semantic-search-alb-573644685.us-east-1.elb.amazonaws.com/llm/embed" ^
     -H "Content-Type: application/json" ^
     -d "{\"text\": \"Hello world\"}"
rem curl -X GET "http://127.0.0.1:8081/health"
