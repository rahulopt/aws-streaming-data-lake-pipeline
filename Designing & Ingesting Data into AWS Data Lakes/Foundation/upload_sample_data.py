import json
import random
import uuid

from datetime import datetime, timedelta
from botocore.exceptions import ClientError

from creating_s3_bucket import s3_client, BUCKET_NAME


def generate_sample_data():
    """Generate sample user event data."""

    events = []

    for days_ago in range(7):

        date = datetime.now() - timedelta(days=days_ago)

        num_events = random.randint(10, 50)

        for _ in range(num_events):

            event = {
                "user_id": str(uuid.uuid4()),
                "event_type": random.choice(
                    ["page_view", "click", "purchase", "signup"]
                ),
                "product_id": str(uuid.uuid4()),
                "timestamp": date.strftime("%Y-%m-%d %H:%M:%S"),
            }

            events.append(event)

    return events


def upload_partitioned_data():
    """Upload sample data with Hive-style time-based partitioning."""

    events = generate_sample_data()

    events_by_date = {}

    # Group events by date
    for event in events:

        date_obj = datetime.strptime(
            event["timestamp"],
            "%Y-%m-%d %H:%M:%S"
        )

        date_key = (
            f"{date_obj.year:04d}/"
            f"{date_obj.month:02d}/"
            f"{date_obj.day:02d}"
        )

        if date_key not in events_by_date:
            events_by_date[date_key] = []

        events_by_date[date_key].append(event)

    # Upload each date partition to S3
    for date_partition, day_events in events_by_date.items():

        year, month, day = date_partition.split("/")

        partition_key = (
            f"raw/user-events/"
            f"year={year}/"
            f"month={month}/"
            f"day={day}/"
            f"events.json"
        )

        json_lines = "\n".join(
            [json.dumps(event) for event in day_events]
        )

        try:

            s3_client.put_object(
                Bucket=BUCKET_NAME,
                Key=partition_key,
                Body=json_lines,
                ContentType="application/json"
            )

            print(
                f"Uploaded {len(day_events)} events "
                f"to {partition_key}"
            )

        except ClientError as e:

            code = e.response["Error"]["Code"]
            message = e.response["Error"].get(
                "Message",
                str(e)
            )

            print(
                f"Error uploading to {partition_key}: "
                f"{code} - {message}"
            )


upload_partitioned_data()