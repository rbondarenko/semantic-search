@echo off
set COMPONENT=%1
set APP=semantic-search

aws cloudformation delete-stack ^
  --stack-name %APP%-%COMPONENT%
@echo on