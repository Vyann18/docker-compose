#!/bin/bash

docker compose exec db psql -U postgres -d barangdb -c "SELECT * FROM barang;"