FROM postgres:14.5-alpine
LABEL authors="dalexander"
# Create a directory for your certificates
RUN mkdir -p /etc/ssl/certs && \
  cd /etc/ssl/certs && \
  # Replace with your server hostname
  openssl req -new -x509 -days 365 -nodes -text -out server.crt \
  -keyout server.key -subj "/CN=$(hostname)" && \
  chmod og-rwx server.key  # Protect the private key

#ENTRYPOINT ["top", "-b"]