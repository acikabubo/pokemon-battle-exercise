## Build docker image
**./scripts/build_docker_image.sh**

## Run docker container
**./scripts/docker_console.sh**

Scripts started with **docker** need to be executed inside docker container (after run docker container script)

## Start server
**./scripts/docker_serve.sh**

[API docs](http://localhost:8000/docs)

## Start pydoc server
**./scripts/docker_pydoc_serve.sh**

[Code docs](http://localhost:8080/)

## Execute unit tests
**./scripts/docker_test.sh**

## Usage

curl -X POST http://127.0.0.1:8000/battle \
    -H 'Content-Type: application/json' \
    -d '{"pokemon1":"pikachu","pokemon2":"charmander"}'
