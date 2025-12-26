# Install UERANSIM (Simulated 5G UE/GNB) in PowerShell

$manifest = @"
apiVersion: v1
kind: ConfigMap
metadata:
  name: ueransim-config
  namespace: open5gs
data:
  gnb.yaml: |
    mcc: '999'
    mnc: '70'
    nci: '0x00000001'
    idLength: 32
    tac: 1
    linkIp: 127.0.0.1
    ngapIp: 127.0.0.1
    gtpIp: 127.0.0.1
    amfConfigs:
      - address: open5gs-amf.open5gs.svc.cluster.local
        port: 38412
    slices:
      - sst: 1
    ignoreStreamIds: true
    gnbId: '0x000001'
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ueransim-gnb
  namespace: open5gs
spec:
  selector:
    matchLabels:
      app: ueransim-gnb
  template:
    metadata:
      labels:
        app: ueransim-gnb
    spec:
      containers:
        - name: gnb
          image: localhost:5000/ueransim-gnb:latest
          imagePullPolicy: IfNotPresent
          command: ["nr-gnb"]
          args: ["-c", "/etc/ueransim/gnb.yaml"]
          volumeMounts:
            - name: config
              mountPath: /etc/ueransim
      volumes:
        - name: config
          configMap:
            name: ueransim-config
"@

$manifest | kubectl apply -f -
