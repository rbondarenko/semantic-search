# Semantic Search project: Search API service

Search API service holds endpoint for semantic search. It's available by `/search` path.
To simplify development Swagger UI for this endpoint can be used. It's available by `/swagger-ui.html` path.

So if Search API service deployed to server with root URL like `https://my-service.com/search-api` then next two 
URLs should be available:
- https://my-service.com/search-api/search -- endpoint for HTTP POST requests
- https://my-service.com/search-api/swagger-ui.html -- Swagger user interface for Search API service 

Search endpoint handles HTTP POST request with JSON body with two required fields: 
- `query` -- free form text for search 
- `limit`-- max number of results

To start service locally next steps can be used:
- run `cm/02-build.cmd` -- it will create/update service Docker image
- run `cm/03-start-local.cmd` -- it will start updated Docker image

To deploy updated Docker image to AWS next steps should be used:
- run `cm/02-build.cmd` -- it will create/update service Docker image
- run `cm/05-deploy.cmd` -- it will deploy updated Docker image to ECR
- update `../infra/03-ecs-params.json` and set correct label for search-api service Docker image
- run `../infra/update.cmd 03 ecs` -- it will update ECS service infrastructure

For more details please check __CM folder structure__ section. 

## Folder structure

- `cm` -- folder has scripts for build and deploy
- `src` -- source codes and tests

## CM folder structure

- `cm/01-create-ecr.cmd` -- create ECR for search-api service
- `cm/02-build.cmd` -- build a docker image for search-api service
- `cm/03-start-local.cmd` -- start search-api service locally by using docker compose
- `cm/04-test-local.cmd` -- test local instance
- `cm/05-deploy.cmd` -- deploy search-api service to AWS
- `cm/05-deploy.sh`-- deploy search-api service to AWS (unix shell version)
- `cm/06-test-remote.cmd` -- test remote instance of search-api service
- `cm/06-test-remote.sh` -- test remote instance of search-api service (unix shell version)
- `cm/docker-compose.yaml` -- docker compose file for local run
- `cm/Dockerfile` -- docker file for service