import boto3

s3 = boto3.client("s3", region_name="us-east-1")
s3.create_bucket(Bucket="my-bucket")
assert "my-bucket" in [b["Name"] for b in s3.list_buckets()["Buckets"]]
