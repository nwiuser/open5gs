# Robust PowerShell script to pull, tag, and load images into Kind
$ClusterName = "telecom-sim"
$Components = "mme", "hss", "sgwc", "sgwu", "pgwc", "pgwu", "pcrf", "amf", "smf", "upf", "nrf", "ausf", "udm", "udr", "nssf", "pcf"
$BaseImage = "gradiant/open5gs:2.7.5"
$WebUIBase = "gradiant/open5gs-webui:2.7.5"
$UeraBase = "gradiant/ueransim:3.2.6"
$MongoBase = "mongo:latest"

Write-Host "Starting manual image load for Kind cluster '$ClusterName'..." -ForegroundColor Cyan

# 1. Pull base images
Write-Host "Pulling base images..." -ForegroundColor Yellow
docker pull $BaseImage
docker pull $WebUIBase
docker pull $UeraBase
docker pull $MongoBase

# 2. Tag and Load Core Components
foreach ($Comp in $Components) {
    $Tag = "localhost:5000/open5gs-$($Comp):latest"
    Write-Host "Preparing $Comp ($Tag)..." -ForegroundColor Yellow
    docker tag $BaseImage $Tag
    kind load docker-image $Tag --name $ClusterName
}

# 3. WebUI
$WebUITag = "localhost:5000/open5gs-webui:latest"
docker tag $WebUIBase $WebUITag
kind load docker-image $WebUITag --name $ClusterName

# 4. UERANSIM
$UeraTag = "localhost:5000/ueransim-gnb:latest"
docker tag $UeraBase $UeraTag
kind load docker-image $UeraTag --name $ClusterName

kind load docker-image $UeraTag --name $ClusterName

# 5. srsRAN
$SrsTag = "localhost:5000/srsran:latest"
docker tag "gradiant/srsran-4g:23_04_1" $SrsTag
kind load docker-image $SrsTag --name $ClusterName

# 6. MongoDB
$MongoTag = "localhost:5000/mongodb:latest"
docker tag $MongoBase $MongoTag
kind load docker-image $MongoTag --name $ClusterName

Write-Host "All images successfully loaded into Kind!" -ForegroundColor Green
