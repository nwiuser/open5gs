#!/bin/bash
# Master script to apply all simulation components

echo "Creating namespaces..."
kubectl create namespace open5gs-4g --dry-run=client -o yaml | kubectl apply -f -
kubectl create namespace open5gs-5g --dry-run=client -o yaml | kubectl apply -f -
kubectl create namespace monitoring --dry-run=client -o yaml | kubectl apply -f -

echo "Deploying 4G Core..."
kubectl apply -f k8s-manifests/4g-core/ --namespace open5gs-4g

echo "Deploying 5G Core..."
kubectl apply -f k8s-manifests/5g-core/ --namespace open5gs-5g

echo "Deploying Monitoring Stack..."
kubectl apply -f k8s-manifests/monitoring/ --namespace monitoring

echo "Deploying UERANSIM (UE/GNB Simulator)..."
./scripts/deploy-ueransim.sh

echo "All components applied. Check status with: kubectl get pods -A"
