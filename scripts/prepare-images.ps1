# Standardized PowerShell script to prepare images for the local registry
# This uses the monolithic gradiant/open5gs image and aliases it for each NF
$Registry = "localhost:5000"
$Components = "mme", "hss", "sgwc", "sgwu", "pgwc", "pgwu", "pcrf", "amf", "smf", "upf", "nrf", "ausf", "udm", "udr", "nssf", "pcf", "webui"
$SourceImage = "gradiant/open5gs:2.7.5" # Stable version

Write-Host "Starting image preparation using gradiant repositories..." -ForegroundColor Cyan

# 1. Pull the source image once
Write-Host "Pulling source image: $SourceImage" -ForegroundColor Yellow
docker pull $SourceImage
if ($LASTEXITCODE -ne 0) { 
    Write-Error "Failed to pull $SourceImage. Check internet connection."
    exit 1
}

# 2. Tag and push for each component
foreach ($Comp in $Components) {
    if ($Comp -eq "webui") {
        $CompSource = "gradiant/open5gs-webui:2.7.5"
        Write-Host "Pulling WebUI image..."
        docker pull $CompSource
        if ($LASTEXITCODE -ne 0) { 
            Write-Warning "Failed to pull dedicated WebUI. Using base image for alias."
            $CompSource = $SourceImage
        }
    } else {
        $CompSource = $SourceImage
    }

    $LocalImage = "$($Registry)/open5gs-$($Comp):latest"
    
    Write-Host "--- Aliasing and pushing: $Comp ---" -ForegroundColor Yellow
    docker tag $CompSource $LocalImage
    docker push $LocalImage
}

# 3. UERANSIM
Write-Host "--- Processing UERANSIM ---" -ForegroundColor Yellow
$UeraImage = "gradiant/ueransim:3.2.6" 
docker pull $UeraImage
if ($LASTEXITCODE -ne 0) {
    Write-Warning "Failed to pull gradiant/ueransim:3.2.6. Trying louisroyer/ueransim..."
    $UeraImage = "louisroyer/ueransim:latest"
    docker pull $UeraImage
}
$UeraLocal = "$($Registry)/ueransim-gnb:latest"
docker tag $UeraImage $UeraLocal
docker push $UeraLocal

docker tag $UeraImage $UeraLocal
docker push $UeraLocal

# 4. srsRAN (4G)
Write-Host "--- Processing srsRAN ---" -ForegroundColor Yellow
$SrsImage = "gradiant/srsran-4g:23_04_1"
docker pull $SrsImage
$SrsLocal = "$($Registry)/srsran:latest"
docker tag $SrsImage $SrsLocal
docker push $SrsLocal

# 5. MongoDB
Write-Host "--- Processing MongoDB ---" -ForegroundColor Yellow
docker pull mongo:latest
docker tag mongo:latest "$Registry/mongodb:latest"
docker push "$Registry/mongodb:latest"

Write-Host "Image preparation complete!" -ForegroundColor Green
