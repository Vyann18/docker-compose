#!/bin/bash

mkdir -p backups

MSYS_NO_PATHCONV=1 docker run --rm \
-v tugas-docker-compose_db-data:/data \
-v $(pwd)/backups:/backup \
alpine \
tar czf /backup/barangdb-backup-$(date +%Y%m%d-%H%M%S).tar.gz -C /data .