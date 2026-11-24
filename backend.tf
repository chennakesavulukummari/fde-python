terraform {
  backend "s3" {
    bucket  = "c3ops-iac-tfstatemgmt"
    key     = "dev/terraform.tfstate"
    region  = "us-east-1"
    #profile = "svc-iac-demo"
  }
}


