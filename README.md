# Semantic Search project

## Goal

Project should implement Semantic Search capability for an e-commerce application.

Project contains two major parts:
- data ingestion and 
- the search engine

Data ingestion part: Ingest the data to a database with vector search capability.

Search Engine: Handle search requests against the database table and produce sorted output.

## Data

For project this data used: https://github.com/luminati-io/eCommerce-dataset-samples/blob/main/amazon-products.csv

## Solution

- Data ingestion pipeline: 
  - reads raw data from S3 in CSV format;
  - process record-by-record by using LLM endpoint for vectors calculation;
  - store data in database.

- Search API service: 
  - handle POST HTTP request with text for search;
  - get vector for passed text by using LLM endpoint;
  - query database with text and vector data;
  - prepare and send response.

## Components

- AWS Lambdas:
  - DB Init lambda -- used for DB initialization after RDF PostgreSQL instance deployment.
  - Data Ingestion lambda -- ingest data for service. Start workinghh when new .csv file would be uploaded to S3 `<bucket>/input/` location.

- ECS Fargate services:
  - LLM service -- holds LLM model. Used for embeddings calculations.
  - Search API service -- hoilds /search endpoint for end-users.

## Project structure

- `infra` -- Cloud Formation stacks and scripts for infrastructuire deployment.
- `dbinit-lambda` -- source code for DB Init lambda.
- `ingestion-lambda` -- source code for Data Ingestion lambda.
- `llm-service` -- source code and configs for LLM service.
- `search-service` -- source code and configs for Search API service.