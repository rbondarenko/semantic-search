for /f "delims=" %%A in ('aws sts get-caller-identity --query Account --output text') do set AWS_ACCOUNT_ID=%%A
set REGION=us-east-1

docker tag search-api:latest %AWS_ACCOUNT_ID%.dkr.ecr.%REGION%.amazonaws.com/search-api:latest
aws ecr get-login-password --region %REGION% | docker login --username AWS --password-stdin %AWS_ACCOUNT_ID%.dkr.ecr.%REGION%.amazonaws.com
docker push %AWS_ACCOUNT_ID%.dkr.ecr.%REGION%.amazonaws.com/search-api:latest
