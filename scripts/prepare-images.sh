#!/bin/bash
# Script to prepare images for the local registry

REGISTRY="localhost:5000"
COMPONENTS=("mme" "hss" "sgwc" "sgwu" "pgwc" "pgwu" "pcrf" "amf" "smf" "upf" "nrf" "ausf" "udm" "udr" "nssf" "pcf" "webui")

echo "Pulling, tagging, and pushing Open5GS images..."

for COMP in "${COMPONENTS[@]}"; do
    IMAGE="open5gs/$COMP:latest"
    LOCAL_IMAGE="$REGISTRY/open5gs-$COMP:latest"
    
    echo "Processing $COMP..."
    docker pull $IMAGE
    docker tag $IMAGE $LOCAL_IMAGE
    docker push $LOCAL_IMAGE
done

# UERANSIM
echo "Processing UERANSIM..."
docker pull ueransim/gnb:latest
docker tag ueransim/gnb:latest $REGISTRY/ueransim-gnb:latest
docker push $REGISTRY/ueransim-gnb:latest

echo "All images pushed to local registry: $REGISTRY"
