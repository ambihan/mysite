#!/bin/sh

docker-compose -f ../local.yml stop
docker-compose -f ../local.yml up --build