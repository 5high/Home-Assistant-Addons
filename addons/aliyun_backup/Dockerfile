ARG BUILD_FROM
FROM $BUILD_FROM
#FROM ubuntu:18.04

# Install requirements for add-on
RUN \
  apk add --no-cache \
    curl tar wget openssl

# Copy data
COPY data/aliyun.py /

# Setup base
RUN chmod a+x /aliyun.py

CMD [ "python3 /aliyun.py" ]
