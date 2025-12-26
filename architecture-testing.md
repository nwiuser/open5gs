# Test de l'Architecture Open5GS 4G

L'infrastructure est maintenant stable au niveau du Plan de Contrôle (CP). Voici comment tester et vérifier la connectivité.

## 1. Vérification des Status
Tous les pods du cœur (HSS, MME, SGW, SMF, PCRF, MongoDB) doivent être en état `Running`.
```bash
kubectl get pods -n open5gs-4g
```

## 2. Vérification de l'Attachement S1AP (eNB <-> MME)
L'eNB (srsRAN) doit se connecter au MME via SCTP. Vérifiez les logs du MME :
```bash
kubectl logs -n open5gs-4g -l app=mme | grep "Added ENB"
```
*Si vous voyez "Added ENB", la connexion radio-cœur est établie.*

## 3. Vérification de l'Attachement UE
Le simulateur srsUE tente de s'attacher automatiquement. Suivez les logs du container `ue` :
```bash
kubectl logs -n open5gs-4g -l app=srsran-4g -c ue --tail=50
```
Vous devriez voir `Attaching UE...`.

## 4. Test du Plan Utilisateur (User Plane)
Une fois l'UE attaché, il crée une interface `tun_srsue`. Vous pouvez tester le ping vers l'extérieur ou vers l'UPF :
```bash
# Dans le container UE
kubectl exec -it -n open5gs-4g $(kubectl get pods -l app=srsran-4g -o name) -c ue -- ping -I tun_srsue 8.8.8.8
```

> [!IMPORTANT]
> **Problème résiduel (UPF)** : L'UPF rencontre actuellement une erreur `ioctl(TUNSETIFF): Operation not permitted`. Cela signifie que malgré le mode `privileged`, le cluster Kind bloque la création de l'interface réseau `ogstun`. Une solution consiste à créer l'interface manuellement sur le nœud worker de Kind.

## 5. Résumé des corrections apportées
- **Core stabilization** : Standardisation des schémas YAML (v2.7.x) et correction des URIs MongoDB.
- **Diameter** : Correction des configurations freeDiameter (HSS/MME/PCRF).
- **Simulator** : Correction des fichiers `sib.conf` (champs obligatoires) et `ue.conf` (identifiants IMSI/IMEI).
