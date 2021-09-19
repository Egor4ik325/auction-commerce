#!/bin/sh

docker container run \
    -p 127.0.0.1:3306:3306 \
    -e MYSQL_DATABASE=mysql \
    -e MYSQL_ROOT_PASSWORD=mysql \
    -e MYSQL_USER=mysql \
    -e MYSQL_PASSWORD=mysql \
    -d \
    mysql