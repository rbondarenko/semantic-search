# Semantic Search project: Data Ingestion lambda

Source code for Inghestion Data lambda function which is doinfg next steps:

- read uploaded CSV file and
- process it record-by-record (calculate embeddings for combination of fields)
- store it to products database

Deployed as a part of inftastructure through Cloud Formation stack (see `../infra/04-ingestion-cfn.yaml`) for more information.