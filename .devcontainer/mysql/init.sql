CREATE USER IF NOT EXISTS 'alpha'@'%' IDENTIFIED BY 'alphapass';
GRANT ALL PRIVILEGES ON *.* TO 'alpha'@'%';
FLUSH PRIVILEGES;

CREATE DATABASE IF NOT EXISTS volunteer;

USE volunteer;

DROP DATABASE IF EXISTS volunteer;

SHOW DATABASES;