# Docker Containerization Strategy

This document outlines the strategy for containerizing the 4G/5G core components.

## Local Registry
- A local Docker registry is used to store simulation images: `localhost:5000`.
- This ensures consistency and allows Kind to pull images locally.

## Image Management
A set of scripts is provided to manage images:
1. `prepare-images.sh`: Pulls official Open5GS and UERANSIM images, tags them for the local registry, and pushes them.
2. `base/Dockerfile`: (Optional) Provides a template for building custom Core images from source if needed.

## Components Containerized
- **4G Core**: HSS, MME, SGW-C, SGW-U, PGW-C, PGW-U, PCRF.
- **5G Core**: AMF, SMF, UPF, NRF, NSSF, AUSF, UDM, UDR, PCF.
- **Simulator**: UERANSIM (GNB/UE).
- **Web UI**: Open5GS Dashboard.
