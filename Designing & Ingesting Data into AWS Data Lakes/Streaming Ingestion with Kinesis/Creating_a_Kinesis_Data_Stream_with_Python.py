import boto3
from botocore.exceptions import ClientError


def create_kinesis_stream():
    """Create a Kinesis Data Stream."""

    sts_client = boto3.client("sts")
    kinesis_client = boto3.client("kinesis")

    account_id = sts_client.get_caller_identity()["Account"]
    stream_name = f"user-event-stream-{account_id}"
    shard_count = 1

    try:
        kinesis_client.create_stream(
            StreamName=stream_name,
            ShardCount=shard_count
        )

        print(f"Creating stream: {stream_name}")
        print("Waiting for stream to become active...")

        waiter = kinesis_client.get_waiter("stream_exists")
        waiter.wait(StreamName=stream_name)

        stream_info = kinesis_client.describe_stream(
            StreamName=stream_name
        )

        description = stream_info["StreamDescription"]
        status = description["StreamStatus"]

        print(f"Stream status: {status}")

        if status == "ACTIVE":
            print("Stream is ready for data!")
            print(f"Stream ARN: {description['StreamARN']}")
            print(f"Shard count: {len(description['Shards'])}")

    except ClientError as e:
        code = e.response["Error"]["Code"]

        if code == "ResourceInUseException":
            print(f"Stream {stream_name} already exists.")
        else:
            message = e.response["Error"].get("Message", str(e))
            print(f"Error creating stream: {code}: {message}")


if __name__ == "__main__":
    create_kinesis_stream()