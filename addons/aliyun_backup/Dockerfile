# Base image is pinned by digest (Alpine 3.24.4, HA base 2026.x) for reproducible builds.
# ghcr.io/home-assistant/{arch}-base:latest -> digest recorded 2026-11-21.
ARG BUILD_FROM
FROM $BUILD_FROM

RUN \
    apk add --no-cache python3 py3-pip git curl bash jq

# Pinned Python dependencies (C2: reproducible builds).
# NOTE: update these pins together with a rebuild+test cycle.
RUN \
    python3 -m pip install --no-cache-dir --break-system-packages \
        aligo==6.2.8 \
        Pillow==13.0.0 \
        schedule==1.2.2 \
        pytz==2026.6 \
        python-dateutil==4.0.0 \
        requests==2.32.5

# Copy root filesystem
COPY rootfs /
