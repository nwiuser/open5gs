Write-Host "Rolling Back Migration: 5G to 4G Core..." -ForegroundColor Yellow
Write-Host "========================================"

Write-Host "Step 1: Destroying 5G Core components..." -ForegroundColor Red
kubectl delete -f C:/Users/NajibNOUISSER/Desktop/newproject/k8s-manifests/5g-core/ --namespace open5gs --ignore-not-found

Write-Host "`nWaiting for pods to terminate (10 seconds)..." -ForegroundColor Gray
Start-Sleep -s 10

Write-Host "`nStep 2: Deploying 4G Core components..." -ForegroundColor Cyan
kubectl apply -f C:/Users/NajibNOUISSER/Desktop/newproject/k8s-manifests/4g-core/ --namespace open5gs

Write-Host "`n========================================"
Write-Host "Rollback Process Initiated Successfully!" -ForegroundColor Green
Write-Host "Monitor 'kubectl get pods -n open5gs' for status changes."
