# https://developers.home-assistant.io/docs/add-ons/configuration#add-on-dockerfile
ARG BUILD_FROM
FROM $BUILD_FROM

# Execute during the build of the image
ARG TEMPIO_VERSION BUILD_ARCH

RUN \
    apk add python3 py3-pip git curl

RUN \
    ln -s /usr/bin/python3 /usr/bin/python \
    && python3 -m pip install --upgrade pip \
    && python3 -m pip install --upgrade Pillow \
    && python3 -m pip install --upgrade schedule \
    && python3 -m pip install --upgrade pytz \
    && python3 -m pip install --upgrade python-dateutil \
    && pip install -U aligo \
    && pip install git+https://github.com/foyoux/aligo.git

# Copy root filesystem
COPY rootfs /
