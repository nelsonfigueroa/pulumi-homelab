import mimetypes
import os

import pulumi
import pulumi_aws as aws

# Create an S3 bucket to hold the website content
bucket = aws.s3.Bucket("nelsons-test-bucket",
    website=aws.s3.BucketWebsiteArgs(
        index_document="index.html",
        error_document="error.html"
    ))

# Turn off "Block all public access"
bucket_public_access_block = aws.s3.BucketPublicAccessBlock(
    "bucketPublicAccessBlock",
    bucket=bucket.bucket,
    block_public_acls=False,
    ignore_public_acls=False,
    block_public_policy=False,
    restrict_public_buckets=False,
    opts=pulumi.ResourceOptions(depends_on=[bucket])
)

# Output the bucket website endpoint
# This is used in the CloudFront Distribution
website_url = pulumi.Output.concat("http://", bucket.website_endpoint)

# Define the bucket policy for public access
bucket_policy = aws.s3.BucketPolicy("bucket-policy",
    bucket=bucket.id,
    policy=bucket.id.apply(lambda bucket_name: f"""
{{
    "Version": "2012-10-17",
    "Statement": [
        {{
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::{bucket_name}/*"
        }}
    ]
}}
"""),
opts=pulumi.ResourceOptions(depends_on=[bucket_public_access_block])
)

# Upload website content to the bucket
content_dir = "html"  # Path to your website content
for file in os.listdir(content_dir):
    file_path = os.path.join(content_dir, file)
    content_type, _ = mimetypes.guess_type(file_path)
    obj = aws.s3.BucketObject(file,
        bucket=bucket.id,
        source=pulumi.FileAsset(file_path),
        content_type=content_type)

# Create a CloudFront distribution for the bucket
cloudfront_distribution = aws.cloudfront.Distribution("cloudfront-distribution",
    origins=[aws.cloudfront.DistributionOriginArgs(
        domain_name=bucket.bucket_regional_domain_name,
        origin_id=website_url,
        s3_origin_config=aws.cloudfront.DistributionOriginS3OriginConfigArgs(
            origin_access_identity=""
        ),
    )],
    enabled=True,
    default_root_object="index.html",
    default_cache_behavior=aws.cloudfront.DistributionDefaultCacheBehaviorArgs(
        allowed_methods=["GET", "HEAD", "OPTIONS"],
        cached_methods=["GET", "HEAD"],
        target_origin_id=website_url,
        forwarded_values=aws.cloudfront.DistributionDefaultCacheBehaviorForwardedValuesArgs(
            query_string=False,
            cookies=aws.cloudfront.DistributionDefaultCacheBehaviorForwardedValuesCookiesArgs(
                forward="none",
            ),
        ),
        viewer_protocol_policy="redirect-to-https",
    ),
    restrictions=aws.cloudfront.DistributionRestrictionsArgs(
        geo_restriction=aws.cloudfront.DistributionRestrictionsGeoRestrictionArgs(
            restriction_type="none"
        ),
    ),
    price_class="PriceClass_100",
    viewer_certificate=aws.cloudfront.DistributionViewerCertificateArgs(
        cloudfront_default_certificate=True,
        minimum_protocol_version="TLSv1.2_2018"
    )
)

# Output the CloudFront distribution URL
pulumi.export("cloudfront_url", cloudfront_distribution.domain_name)
pulumi.export("cloudfront_urn", cloudfront_distribution.urn)
