# aws_s3_bucket resource name
# data-lake-bucket bucket name that we chose
# Bucket and ACL are the argument types for our resource
resource "aws_s3_bucket" "data-lake-bucket" {
    bucket = "${var.bucket_name}"

    versioning {
        enabled = true
    }

    lifecycle_rule {
        id = "remove_old_files"
        enabled = true

        expiration {
            days = 30
        }
    }

    force_destroy = true
}
