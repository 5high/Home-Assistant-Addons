# https://developers.home-assistant.io/docs/add-ons/configuration#add-on-dockerfile
ARG BUILD_FROM
FROM $BUILD_FROM

# Execute during the build of the image
ARG TEMPIO_VERSION BUILD_ARCH
RUN \
    sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories

RUN \
    apk add python3 py3-pip git curl

RUN \
    curl -s https://gitlab.com/ineo6/hosts/-/raw/master/hosts?ref_type=heads >> /etc/hosts

RUN \
    ln -s /usr/bin/python3 /usr/bin/python \
    && python3 -m pip install -i https://mirrors.aliyun.com/pypi/simple/ --upgrade pip \
    && python3 -m pip install -i https://mirrors.aliyun.com/pypi/simple/ --upgrade Pillow \
    && python3 -m pip install -i https://mirrors.aliyun.com/pypi/simple/ --upgrade schedule \
    && python3 -m pip install -i https://mirrors.aliyun.com/pypi/simple/ --upgrade pytz \
    && python3 -m pip install -i https://mirrors.aliyun.com/pypi/simple/ --upgrade python-dateutil \
    && pip install git+https://github.com/5high/aligo.git

# Copy root filesystem
COPY rootfs /
