#!/bin/bash

echo "=================================="
echo "WEB -> API"
echo "=================================="

docker compose exec -T web python -c "
import socket
try:
    socket.create_connection(('api',8080),timeout=5)
    print('SUCCESS: web dapat akses api')
except Exception as e:
    print('FAILED:', e)
"

echo ""
echo "=================================="
echo "API -> DB"
echo "=================================="

docker compose exec -T api python -c "
import socket
try:
    socket.create_connection(('db',5432),timeout=5)
    print('SUCCESS: api dapat akses db')
except Exception as e:
    print('FAILED:', e)
"

echo ""
echo "=================================="
echo "WEB -> DB (expected failed)"
echo "=================================="

docker compose exec -T web python -c "
import socket
try:
    socket.create_connection(('db',5432),timeout=5)
    print('UNEXPECTED SUCCESS')
except Exception as e:
    print('EXPECTED FAILED:', e)
"