FROM mariadb:10.6
LABEL authors="dalexander"
COPY .devcontainer/mariadb/init.sql /docker-entrypoint-initdb.d/
#COPY .devcontainer/mariadb/my.cnf /etc/mysql/mariadb.conf.d/
#COPY .devcontainer/mariadb/init.sql /mysql_files/
#COPY .devcontainer/mariadb/entrypoint.sh /entrypoint.sh
#RUN chmod +x /docker-entrypoint-initdb.d/init.sql \
#    && chmod +x /entrypoint.sh

EXPOSE 3307

CMD ["mysqld", "--init-file", "/docker-entrypoint-initdb.d/init.sql"]


