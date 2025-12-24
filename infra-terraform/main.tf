terraform {
  required_providers {
    kind = {
      source  = "tehcyx/kind"
      version = "0.7.0"
    }
  }
}

provider "kind" {}

resource "kind_cluster" "telecom_cluster" {
  name            = "4g-5g-migration"
  node_image      = "kindest/node:v1.31.0"
  wait_for_ready  = true
  
  # Using the block syntax as requested by the error
  kind_config {
    kind        = "Cluster"
    api_version = "kind.x-k8s.io/v1alpha4"
    
    node {
      role = "control-plane"
      extra_port_mappings {
        container_port = 30041
        host_port      = 30041
        protocol       = "udp"
      }
      extra_port_mappings {
        container_port = 30041
        host_port      = 30041
        protocol       = "tcp"
      }
    }
    
    node {
      role = "worker"
    }
  }
}

output "kubeconfig" {
  value = kind_cluster.telecom_cluster.kubeconfig
}
