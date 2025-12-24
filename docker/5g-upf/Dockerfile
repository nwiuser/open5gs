# Dockerfile for 5G UPF (User Plane Function)
FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python3-pip \
    flex \
    bison \
    git \
    libsctp-dev \
    libgnutls28-dev \
    libgcrypt20-dev \
    libssl-dev \
    libidn11-dev \
    libmongoc-dev \
    libbson-dev \
    libyaml-dev \
    libmicrohttpd-dev \
    libcurl4-gnutls-dev \
    libnghttp2-dev \
    libtins-dev \
    meson \
    ninja-build \
    build-essential \
    && apt-get clean

LABEL component="upf"
LABEL network="5g"

# ENTRYPOINT ["open5gs-upfd", "-c", "/etc/open5gs/upf.yaml"]
