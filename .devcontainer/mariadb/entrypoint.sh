#!/bin/bash
set -e

## Wait for MariaDB to be ready
#until mysqladmin ping -h 127.0.0.1 --silent 2>&1; do
#  echo 'waiting for mariadb . . .'
#  sleep 2
#done

# Load the SQL script
mysql -u root -p"$MYSQL_ROOT_PASSWORD" < /docker-entrypoint-initdb.d/init.sql

# Run the main command
exec "$@"
