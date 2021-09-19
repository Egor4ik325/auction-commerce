#!/bin/sh

# Create and start a Django webapp container from project image
docker container run \
    -p 127.0.0.1:8000:8000 \
    -v "$(pwd)":/usr/app/src \
    -d \
    --name auction-webapp \
    auction-webapp
