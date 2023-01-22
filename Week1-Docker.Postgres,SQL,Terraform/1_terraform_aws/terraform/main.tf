provider "aws" {
    shared_credentials_files = ["~/.aws/credentials"]
    region = var.aws_region
}

module "s3_bucket" {
    source = "../../"
}

# SNOWFLAKE
terraform {
  required_providers {
    snowflake = {
      source  = "Snowflake-Labs/snowflake"
      version = "~> 0.35"
    }
  }
}

provider "snowflake" {
  role = "SYSADMIN"
}

resource "snowflake_database" "db" {
  name = "TF_DEMO"
}