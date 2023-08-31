#!/bin/bash
docker run --rm -it --name pokemon-battle \
    -v $(pwd):/project:delegated \
    -p 8000:80 -p 8080:8080 \
    pokemon-battle \
    bash
