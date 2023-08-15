import re
import json
import boto3
import random
from botocore.exceptions import ClientError


def lambda_handler(event, context):
    create_unique_s3_bucket(3, "a_324S..d%#--s3alias")


def create_unique_s3_bucket(space_id, space_name):
    while True:
        if create_s3_bucket(space_id, space_nam):
            break


def create_s3_bucket(space_id, space_name):
    try:
        bucket_name = (
            "id-"
            + str(space_id)
            + "-"
            + transform_string(space_name)
            + "-"
            + str(get_random_3_digit_number())
        )
        s3_client = boto3.client("s3")
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
