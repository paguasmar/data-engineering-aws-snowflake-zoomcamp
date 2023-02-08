# var.tf is used to declare values of variables. We can either provide a default value to be used when needed or ask for value during execution.
variable "bucket_name" {
    default = "dtc-data-lake"
}

variable "aws_region" {
    default = "us-east-1"
}