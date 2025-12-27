# Master script to apply all simulation components in PowerShell

Write-Host "Creating namespaces..." -ForegroundColor Cyan
kubectl create namespace open5gs --dry-run=client -o yaml | kubectl apply -f -
# kubectl create namespace monitoring --dry-run=client -o yaml | kubectl apply -f -

Write-Host "Applying Base Manifests (Certs, etc.)..." -ForegroundColor Cyan
kubectl apply -f k8s-manifests/00-certs.yaml --namespace open5gs
kubectl apply -f k8s-manifests/00-upf-scripts.yaml --namespace open5gs

Write-Host "Deploying 4G Core..." -ForegroundColor Cyan
kubectl apply -f k8s-manifests/4g-core/ --namespace open5gs

# Write-Host "Deploying 5G Core..." -ForegroundColor Cyan
# kubectl apply -f k8s-manifests/5g-core/ --namespace open5gs

# Write-Host "Deploying Monitoring Stack..." -ForegroundColor Cyan
# kubectl apply -f k8s-manifests/monitoring/ --namespace monitoring

# Write-Host "Deploying UERANSIM (UE/GNB Simulator)..." -ForegroundColor Cyan
# if (Test-Path ".\scripts\deploy-ueransim.ps1") {
#     .\scripts\deploy-ueransim.ps1
# } else {
#     Write-Warning "scripts/deploy-ueransim.ps1 not found, trying .sh (might fail on Windows)..."
#     .\scripts\deploy-ueransim.sh
# }

Write-Host "`nAll components applied. Check status with: kubectl get pods -A" -ForegroundColor Green
