from botocore.exceptions import ClientError
from creating_s3_bucket import s3_client, BUCKET_NAME


def verify_uploaded_files():
    """Show what files and folders were actually created in S3."""

    try:
        response = s3_client.list_objects_v2(
            Bucket=BUCKET_NAME
        )

    except ClientError as e:
        code = e.response["Error"]["Code"]
        message = e.response["Error"].get(
            "Message",
            str(e)
        )

        print(f"Error listing objects: {code} - {message}")
        raise

    print("\nFiles actually created in S3:")

    if "Contents" in response:
        for obj in response["Contents"]:
            print(
                f"  {obj['Key']} "
                f"({obj['Size']} bytes)"
            )
    else:
        print("  No files found")


verify_uploaded_files()
