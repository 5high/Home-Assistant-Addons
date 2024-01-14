ARG BUILD_FROM
FROM $BUILD_FROM
#FROM ubuntu:18.04

# Install requirements for add-on
RUN \
  apk add --no-cache \
    curl tar wget openssl python3 python3-pip

# Copy data
COPY data/run.sh /

RUN pip install -U aligo \
    && pip install git+https://github.com/foyoux/aligo.git
    
# Setup base
RUN chmod a+x /aliyun.py

CMD [ "/run.sh" ]
