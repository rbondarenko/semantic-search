@echo off
setlocal

:: ==== CONFIGURATION ====
set PREFIX=%1
set COMPONENT=%2
set APP=semantic-search
set REGION=us-east-1

set STACK_NAME=%APP%-%COMPONENT%
set TEMPLATE_FILE=%PREFIX%-%COMPONENT%-cfn.yaml
set PARAMS_FILE=%PREFIX%-%COMPONENT%-params.json

:: ==== CHECK IF STACK EXISTS ====
echo Checking if stack %STACK_NAME% exists...
aws cloudformation describe-stacks --stack-name %STACK_NAME% --region %REGION% >nul 2>&1

if %ERRORLEVEL% EQU 0 (
    echo Stack exists. Updating...
    aws cloudformation update-stack ^
        --stack-name %STACK_NAME% ^
        --template-body file://%TEMPLATE_FILE% ^
        --parameters file://%PARAMS_FILE% ^
        --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM ^
        --region %REGION%

    if %ERRORLEVEL% NEQ 0 (
        echo Update failed or no updates were needed.
    ) else (
        echo Update initiated. Use describe-stacks or wait-stack-update-complete to track progress.
    )
) else (
    echo Stack does not exist. Creating...
    aws cloudformation create-stack ^
        --stack-name %STACK_NAME% ^
        --template-body file://%TEMPLATE_FILE% ^
        --parameters file://%PARAMS_FILE% ^
        --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM ^
        --region %REGION%

    if %ERRORLEVEL% NEQ 0 (
        echo Create failed.
    ) else (
        echo Create initiated. Use describe-stacks or wait-stack-create-complete to track progress.
    )
)

endlocal
