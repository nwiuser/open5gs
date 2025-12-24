# Base Dockerfile for Open5GS components
FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-setuptools \
    python3-wheel \
    ninja-build \
    build-essential \
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
    libidn11-dev \
    cmake \
    meson \
    && apt-get clean

# Clone Open5GS (simplified for this simulation)
# In a real scenario, we would build from source or use specific tags.
# Here we will use the already existing Docker images as base but define the structure.
# For this lab, we will create a wrapper structure to manage them.

LABEL description="Open5GS Base Image for 4G/5G Migration Simulation"
