import boto3
from botocore.exceptions import ClientError

# Create AWS clients
s3_client = boto3.client("s3")
sts_client = boto3.client("sts")

# Get AWS account ID
account_id = sts_client.get_caller_identity()["Account"]

# S3 bucket names must be globally unique
BUCKET_NAME = f"my-data-lake-{account_id}"


def create_bucket():
    """Create S3 bucket for data lake."""

    # Check whether bucket already exists
    try:
        s3_client.head_bucket(Bucket=BUCKET_NAME)
        print(f"Bucket {BUCKET_NAME} already exists")
        return

    except ClientError:
        pass

    # Create bucket
    try:
        s3_client.create_bucket(Bucket=BUCKET_NAME)
        print(f"Created bucket: {BUCKET_NAME}")

    except ClientError as e:
        code = e.response["Error"]["Code"]
        message = e.response["Error"].get(
            "Message",
            str(e)
        )

        print(f"Error creating bucket: {code} - {message}")


create_bucket()