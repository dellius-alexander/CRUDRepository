FROM mysql:8.0
LABEL authors="dalexander"
#ENV MYSQL_UNIX_PORT /var/run/mysqld/mysqld.sock
ENV MYSQL_TCP_PORT 3306
ENV MYSQL_ROOT_PASSWORD adminpassword
#RUN mkdir -p /var/log/mysql && \
#    touch /var/log/mysql/error.log
#RUN chown -R mysql:mysql /var/log/mysql
COPY .devcontainer/mysql/init.sql /docker-entrypoint-initdb.d/init.sql
#COPY .devcontainer/mysql/my.cnf /etc/mysql/conf.d/
#COPY .devcontainer/mysql/init.sql /mysql_files/
CMD ["mysqld", "--init-file", "/docker-entrypoint-initdb.d/init.sql"]
