# ---------------------------------------------
# Admins group
# ---------------------------------------------

aws iam create-group --group-name Admins
aws iam attach-group-policy \
  --group-name Admins \
  --policy-arn arn:aws:iam::aws:policy/AdministratorAccess

# ---------------------------------------------
# User 
# ---------------------------------------------

aws iam create-user --user-name dev-admin
aws iam add-user-to-group --user-name dev-admin --group-name Admins
aws iam create-login-profile \
  --user-name dev-admin \
  --password 'ChangeMeNow!123' \
  --password-reset-required
# Enforce a strong password policy (min length 14, require uppercase/lowercase/number/symbol) 
aws iam update-account-password-policy \
  --minimum-password-length 14 \
  --require-symbols \
  --require-numbers \
  --require-uppercase-characters \
  --require-lowercase-characters \
  --allow-users-to-change-password \
  --max-password-age 90 \
  --password-reuse-prevention 5

# ---------------------------------------------
# secrets manager
# ---------------------------------------------

aws secretsmanager create-secret \
  --name prod/db-creds \
  --secret-string '{"username":"dbuser","password":"StrongPass!23"}'

# ---------------------------------------------
# ecsAppRole
# ---------------------------------------------

aws iam create-role \
  --role-name ecsAppRole \
  --assume-role-policy-document file://ecs-trust.json
aws iam attach-role-policy \
  --role-name ecsAppRole \
  --policy-arn arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly
aws iam attach-role-policy \
  --role-name ecsAppRole \
  --policy-arn arn:aws:iam::aws:policy/CloudWatchLogsFullAccess

# ---------------------------------------------
# lambdaIngestRole
# ---------------------------------------------

aws iam create-policy \
  --policy-name LambdaIngestPolicy \
  --policy-document file://lambda-ingest-policy.json
aws iam attach-role-policy \
  --role-name lambdaIngestRole \
  --policy-arn arn:aws:iam::776567512212:policy/LambdaIngestPolicy

# ---------------------------------------------
# RDS
# ---------------------------------------------

aws rds create-db-instance \
  --db-instance-identifier products-db \
  --engine postgres \
  --engine-version 15.3 \
  --db-instance-class db.t3.micro \
  --allocated-storage 20 \
  --master-username admin \
  --master-user-password MyPass123 \
  --backup-retention-period 0 \
  --no-publicly-accessible

# ---------------------------------------------
# ECS cluster
# ---------------------------------------------

aws ecs create-cluster \
  --cluster-name semantic-search-cluster

# Register and run tasks for LLM and API (after pushing Docker images to ECR)...
# And similarly, use 
aws ecs register-task-definition ...
aws ecs create-service ...
# Use... 
aws s3 cp ... 
# ...to upload data and 
aws lambda update-function-code ...
# ...to deploy Lambda code.


# bucket
aws s3 mb s3://my-product-bucket

# copy data to bucket
aws s3 cp products.json s3://my-product-bucket/
