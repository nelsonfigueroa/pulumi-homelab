import pulumi
import pulumi_aws as aws
import pulumi_gcp as gcp

# replace this with your GCP Project ID
gcp_project_id = "0000000000"

# define AWS S3 Bucket
aws_s3_bucket = aws.s3.Bucket("aws-bucket")

# define GCP storage bucket
gcp_bucket = gcp.storage.Bucket("gcp-bucket",
                                location="US",
                                project=gcp_project_id)

# Export the bucket names
pulumi.export("aws_bucket_name", aws_s3_bucket.id)
pulumi.export("gcp_bucket_name", gcp_bucket.name)
