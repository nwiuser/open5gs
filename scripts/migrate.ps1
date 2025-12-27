Write-Host "Starting Core Migration: 4G to 5G..." -ForegroundColor Yellow
Write-Host "========================================"

Write-Host "Step 1: Destroying 4G Core components..." -ForegroundColor Red
# Using --ignore-not-found to avoid errors if some components are already gone
kubectl delete -f C:/Users/NajibNOUISSER/Desktop/newproject/k8s-manifests/4g-core --namespace open5gs --ignore-not-found

Write-Host "`nWaiting for pods to terminate (10 seconds)..." -ForegroundColor Gray
Start-Sleep -s 10

Write-Host "Creating namespaces..." -ForegroundColor Cyan
kubectl create namespace open5gs --dry-run=client -o yaml | kubectl apply -f -

Write-Host "`nStep 2: Deploying 5G Core components..." -ForegroundColor Cyan
kubectl apply -f C:/Users/NajibNOUISSER/Desktop/newproject/k8s-manifests/5g-core/ --namespace open5gs

Write-Host "`n========================================"
Write-Host "Migration Process Initiated Successfully!" -ForegroundColor Green
Write-Host "Monitor 'kubectl get pods -n open5gs' for status changes."
