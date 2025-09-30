@echo off
set HOST=semantic-search-alb-1395423697.us-east-1.elb.amazonaws.com
rem curl -X GET "http://%HOST%/search/actuator/health"
curl -X POST "http://%HOST%/search/search" ^
     -H "Content-Type: application/json" ^
     -d "{\"query\": \"car tire\", \"limit\": 5}"
@echo on