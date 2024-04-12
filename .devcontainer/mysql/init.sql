CREATE DATABASE IF NOT EXISTS volunteer;
CREATE USER IF NOT EXISTS 'alpha'@'%' IDENTIFIED BY 'alphapass';
GRANT ALL PRIVILEGES ON volunteer.* TO 'alpha'@'%';
FLUSH PRIVILEGES;