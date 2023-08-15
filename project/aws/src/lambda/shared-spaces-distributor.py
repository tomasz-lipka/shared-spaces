# This lambda function copies an incoming object from a temp bucket to a destination bucket.
# Every space has its own destination bucket.
# The incoming object must be named following the convention: <space_id>-<share_id>
import re
import json
import boto3
import random
from botocore.exceptions import ClientError

s3_client = boto3.client("s3")
source_bucket = "shared-spaces-temp"
bucket_prefix = "space-id-"


def lambda_handler(event, context):
    try:
        for record in event["Records"]:
            object_key = record["s3"]["object"]["key"]
            space_id = get_space_id(object_key)
            bucket_name = create_bucket_name(space_id)
            actual_bucket = find_bucket(bucket_name)

            if not actual_bucket:
                actual_bucket = add_random_suffix(bucket_name)
                create_unique_bucket(actual_bucket)
            copy_object(actual_bucket, object_key)
            delete_object_from_temp(object_key)

    except ClientError as e:
        print("Error Message: {}".format(e))


def create_unique_bucket(bucket_name):
    while True:
        if create_bucket(bucket_name):
            break


def create_bucket(bucket_name):
    try:
        s3_client.create_bucket(Bucket=bucket_name)
        return True
    except ClientError as e:
        if e.response["Error"]["Code"] == "BucketAlreadyExists":
            return False


def get_random():
    return random.randint(10000, 99999)


def copy_object(destination_bucket, object_key):
    copy_source = {"Bucket": source_bucket, "Key": object_key}
    s3_client.copy_object(
        CopySource=copy_source, Bucket=destination_bucket, Key=object_key
    )
    
    
def delete_object_from_temp(object_key):
    s3_client.delete_object(Bucket=source_bucket, Key=object_key)


def find_bucket(bucket_name):
    response = s3_client.list_buckets()

    for bucket in response["Buckets"]:
        if bucket["Name"].startswith(bucket_name):
            return bucket["Name"]
    return None


def create_bucket_name(space_id):
    return bucket_prefix + str(space_id)


def add_random_suffix(bucket_name):
    return bucket_name + "-" + str(get_random())


def get_space_id(object_key):
    return object_key.split("-")[0]
