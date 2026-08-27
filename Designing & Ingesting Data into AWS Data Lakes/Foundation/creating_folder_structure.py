from creating_s3_bucket import s3_client, BUCKET_NAME
from botocore.exceptions import ClientError


def create_folder_structure():
    """Create the data lake folder structure."""

    folders = [
        "raw/user-events/",
        "raw/product-catalog/",
        "processed/user-events/",
        "processed/product-catalog/",
        "curated/analytics/",
        "curated/reports/"
    ]

    for folder in folders:
        try:
            # Create empty object to represent folder
            s3_client.put_object(
                Bucket=BUCKET_NAME,
                Key=folder,
                Body=""
            )

            print(f"Created folder: {folder}")

        except ClientError as e:
            code = e.response["Error"]["Code"]
            message = e.response["Error"].get(
                "Message",
                str(e)
            )

            print(f"Error creating folder {folder}: {code} - {message}")


create_folder_structure()

#Security Note(Production)
# In a real production data lake, you shoud treat your s3 bucket as sensitive infrastructure:
#Block all public access 
#Enable encryption at rest
#Use least-privilege access control
#consider enforcing TLS-only requests in the bucket policy