# Semantic Search project: Search API service

## Folder structure

- `cm` -- folder has scripts for build and deploy
- `src` -- source codes and tests

## CM folder structure

- `01-create-ecr.cmd` -- create ECR for search-api service
- `02-build.cmd` -- build a docker image for seaerch-api service
- `03-start-local.cmd` -- start search-api service locally by using docker compose
- `04-test-local.cmd` -- test local instance
- `05-deploy.cmd` -- deploy search-api service to AWS
- `05-deploy.sh`-- deploy search-api service to AWS (unix shell version)
- `06-test-remote.cmd` -- test remote instance of search-api service
- `06-test-remote.sh` -- test remote instance of search-api service (unix shell version)
- `docker-compose.yaml` -- docker compose filem for local run
- `Dockerfile` -- docker file for service