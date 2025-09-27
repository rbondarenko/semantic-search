#!/bin/sh
curl -v \
 --header "Content-Type: application/json" \
 --request POST \
 --data '{"text":"xyz"}' \
 http://127.0.0.1:8081/embed
