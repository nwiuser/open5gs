#!/bin/bash
# Install UERANSIM (Simulated 5G UE/GNB)

cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: ConfigMap
metadata:
  name: ueransim-config
  namespace: open5gs-5g
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
      - address: open5gs-amf.open5gs-5g.svc.cluster.local
        port: 38412
    slices:
      - sst: 1
    gnbId: '0x000001'
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ueransim-gnb
  namespace: open5gs-5g
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
          image: ueransim/gnb:latest
          volumeMounts:
            - name: config
              mountPath: /etc/ueransim
      volumes:
        - name: config
          configMap:
            name: ueransim-config
EOF
