#!/bin/bash

docker run --name mariadb -e MYSQL_ROOT_PASSWORD=claveroot \
    -v $(pwd)/basedatos:/var/lib/mysql \
    --rm --network pruebas -d mariadb
