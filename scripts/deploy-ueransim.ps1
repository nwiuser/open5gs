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
    linkIp: 0.0.0.0
    ngapIp: 0.0.0.0
    gtpIp: 0.0.0.0
    amfConfigs:
      - address: open5gs-amf.open5gs.svc.cluster.local
        port: 38412
    slices:
      - sst: 1
    ignoreStreamIds: true
    gnbId: '0x000001'
  ue.yaml: |
    supi: 'imsi-999700000000001'
    mcc: '999'
    mnc: '70'
    key: '465B5CE8B199B49FAA5F0A2EE238A6BC'
    op: 'E8ED289DEBA952E4283B54E88E6183CA'
    opType: 'OPC'
    amf: '8000'
    gnbSearchList:
      - ueransim-gnb
    sessions:
      - type: 'IPv4'
        apn: 'internet'
        slice:
          sst: 1
    routingIndicator: '0000'
    
    # UAC Access Identities Configuration
    uacAic:
      mps: false
      mcs: false
    # UAC Access Control Class
    uacAcc:
      normalClass: 0
      class11: false
      class12: false
      class13: false
      class14: false
      class15: false

    integrity:
      IA1: true
      IA2: true
      IA3: true
    ciphering:
      EA1: true
      EA2: true
      EA3: true
    integrityMaxRate:
      uplink: 'full'
      downlink: 'full'
---
apiVersion: v1
kind: Service
metadata:
  name: ueransim-gnb
  namespace: open5gs
spec:
  selector:
    app: ueransim-gnb
  ports:
    - name: radio
      port: 4997
      protocol: UDP
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ueransim-ue
  namespace: open5gs
spec:
  selector:
    matchLabels:
      app: ueransim-ue
  template:
    metadata:
      labels:
        app: ueransim-ue
    spec:
      containers:
        - name: ue
          image: localhost:5000/ueransim-gnb:latest
          imagePullPolicy: IfNotPresent
          command: ["nr-ue"]
          args: ["-c", "/etc/ueransim/ue.yaml"]
          securityContext:
            privileged: true
            capabilities:
              add: ["NET_ADMIN"]
          volumeMounts:
            - name: config
              mountPath: /etc/ueransim
      volumes:
        - name: config
          configMap:
            name: ueransim-config
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