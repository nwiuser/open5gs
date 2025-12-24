# PowerShell script to load images from local registry into Kind
$Images = docker images --format "{{.Repository}}:{{.Tag}}" | Select-String "localhost:5000"

Write-Host "Loading images into Kind cluster 'telecom-sim'..." -ForegroundColor Cyan

foreach ($Img in $Images) {
    Write-Host "Loading: $Img" -ForegroundColor Yellow
    kind load docker-image $Img --name telecom-sim
}

Write-Host "All images loaded into Kind!" -ForegroundColor Green
