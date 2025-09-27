# Semantic Search project: Infrastructure

## Infrastructure components
For deployment purposed project infrastructure was divided to next layers:
- Users
- VPC
- DB
- ECS
- Ingestion

Infrastructure components should be deployed in that order.

## Layers Description
### Users layer
#### Purpose
Manage IAM users and groups.

#### Files
- `infra/00-users-cfn.yaml` - CloudFoundation stack definition
- `infra/00-users-params.json` - parameters for stack deployment

#### Notes
Initially have been implemented manually by using AWS Console.

### VPC layer
#### Purpose
Manage VPC and network settings

#### Files
- `infra/01-vpc-cfn.yaml` - CloudFormation stack definition
- `infra/01-vpc-params.json` - parameters for stack deployment

### DB Layer
#### Purpose
Manage database for project: RDS PostgreSQL instance + pgvector, DB Secrets, DB bootstrap lambda

#### Files
- `infra/02-db-cfn.yaml` - CloudFormation stack definition
- `infra/02-db-params.json` - parameters for stack deployment

#### Notes
Stack deployment parameters have to be updated before use.

### ECS layer
#### Purpose
Manage Search API endpoints and LLM model endpoints.

#### Files
- `infra/03-ecs-cfn.yaml` - CloudFormation stack definition
- `infra/03-ecs-params.json` - parameters for stack deployment

#### Notes
1. Before this layer deployment we have to build and publish Docker images for both: LLM Service and 
Search API services. Please see `../llm-service` and `../search-api` folders for more information.

2. Stack deployment parameters have to be updated before use.

### Ingestion layer
#### Purpose
Manage data ingestion pipeline with S3 bucket and Lambda

#### Files
- `infra/04-ingestion-cfn.yaml` - CloudFormation stack definition
- `infra/04-ingestion-params.json` - parameters for stack deployment

#### Notes
Stack deployment parameters have to be updated before use.

## Stacks development

For development can be used CloudFormation linter.

```shell
pip install cfn-lint
cfn-lint ./**.yaml
```

## Stacks deployment

For stacks deployment next script can be used:

```shell
update.cmd <order_number> <component_name>
```

where:
- order number is a 2 digits from stack name, like "03" for ECS stack for example.
- conmponentn name - word after order number and can be one of this: "vpc", "db", "ecs" or "ingestion"

so for deploy DB for example, a command line would be like:

```shell
update.cmd 02 db
```

## Stacks delete

If you want delete stack, please remember about dependencies between it (see xxx-params.json) and delete first all stacks which is depends from given stack.

To delete you can use next command:

```shell
delete <component_name>
```

where componentn name is: vpc, db, ecs or ingestion.