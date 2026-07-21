#!/bin/bash

FILE=$1

docker compose down -v

docker volume create tugas-docker-compose_db-data

MSYS_NO_PATHCONV=1 docker run --rm \
-v tugas-docker-compose_db-data:/data \
-v $(pwd):/backup \
alpine \
sh -c "cd /data && tar xzf /backup/$FILE"

docker compose up -d