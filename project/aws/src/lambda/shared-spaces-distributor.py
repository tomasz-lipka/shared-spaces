import re
import json
import boto3
import random
from botocore.exceptions import ClientError

s3_client = boto3.client("s3")


def lambda_handler(event, context):
    try:
        # create_unique_bucket(3, "a_324S..d%#--s3alias")
        copy_object(event, "shared-spaces-temp", "id-3-a324sds3alias-849")
    except botocore.exceptions.ClientError as e:
        print("Error Message: {}".format(e))


def create_unique_bucket(space_id, space_name):
    while True:
        if create_bucket(space_id, space_name):
            break


def create_bucket(space_id, space_name):
    try:
        bucket_name = (
            "id-"
            + str(space_id)
            + "-"
            + transform_string(space_name)
            + "-"
            + str(get_random_3_digit_number())
        )
        s3_client.create_bucket(Bucket=bucket_name)
        return True
    except ClientError as e:
        if e.response["Error"]["Code"] == "BucketAlreadyExists":
            return False


def transform_string(input):
    # Truncate the string to a maximum length of n characters
    input = input[:30]

    # Make lowercase
    input = input.lower()

    # Use a regular expression to clean characters that are not lower case letters or numbers
    input = re.sub(r"[^a-z0-9]", "", input)

    return input


def get_random_3_digit_number():
    return random.randint(100, 999)


def copy_object(event, source_bucket, destination_bucket):
    for record in event["Records"]:
        object_key = record["s3"]["object"]["key"]
        copy_source = {"Bucket": source_bucket, "Key": object_key}
        s3_client.copy_object(
            CopySource=copy_source, Bucket=destination_bucket, Key=object_key
        )
