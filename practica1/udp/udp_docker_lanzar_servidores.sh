#!/bin/bash

for nombre in servidor_hola1 servidor_hola2 servidor_hola3; do
    docker run -d --rm --name $nombre --network pruebas \
        -v $(pwd):/app python:3.7 python /app/udp_servidor6_broadcast.py
done
