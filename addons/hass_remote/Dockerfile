ARG BUILD_FROM
FROM $BUILD_FROM
#FROM ubuntu:18.04

# Install requirements for add-on
RUN \
  apk add --no-cache \
    curl tar wget openssl

# Copy data
COPY data/run.sh /

# Setup base
RUN chmod a+x /run.sh \
    && if [[ "$(arch)" = "aarch64" ]]; then curl -L -s "https://sumju.net/linux_arm64_client.tar.gz" | tar -zxv  -C /usr/bin; fi \
    && if [[ "$(arch)" = "x86_64" ]]; then curl -L -s "https://sumju.net/linux_amd64_client.tar.gz" | tar -zxv -C /usr/bin; fi

CMD [ "/run.sh" ]
