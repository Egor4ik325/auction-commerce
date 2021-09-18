#!/bin/sh

# Create and start a container
docker container run \
    -p 127.0.0.1:8000:8000 \
    -d \
    --name auction-webapp \
    auction-webapp
