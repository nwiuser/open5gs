# Dockerfile for 4G MME (Mobility Management Entity)
FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-setuptools \
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

# In a real build, we would git clone and compile here.
# For simulation purposes, we'll label it as the build-from-source version.
LABEL component="mme"
LABEL network="4g"

# Example config copy (to be mounted)
# COPY mme.yaml /etc/open5gs/mme.yaml

# ENTRYPOINT ["open5gs-mmed", "-c", "/etc/open5gs/mme.yaml"]
