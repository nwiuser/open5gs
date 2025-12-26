$ns = "open5gs-4g"
mkdir logs_$ns -Force

kubectl get pods -n $ns -o jsonpath="{.items[*].metadata.name}" |
  % {
      $pod = $_
      $file = "logs_$ns\$pod.log"
      kubectl logs -n $ns $pod -c all > $file
      Write-Host "Logs de $pod → $file" }