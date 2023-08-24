import os
import datetime
from flask_login import current_user
import boto3
import botocore.exceptions

from ..media.media_service import MediaService
from ..service.validator_helper import ValidatorHelper


class AwsService(MediaService):

    FILE_FORMAT = '.jpg'

    def __init__(self, queue_url, s3_temp_bucket, validator: ValidatorHelper, ):
        self.queue_url = queue_url
        self.s3_temp_bucket = s3_temp_bucket
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
        )
        self.validator = validator

    def upload_image(self, file, space_id, share_id):
        space = self.validator.validate_space(space_id)
        share = self.validator.validate_share(share_id)
        self.validator.validate_share_owner(
            share,
            int(current_user.get_id())
        )
        object_key = str(space.id) + '-' + str(share.id) + self.FILE_FORMAT
        self.s3_client.upload_fileobj(
            file,
            self.s3_temp_bucket,
            object_key
        )
        self.send_file_name_to_sqs(object_key)

    def get_image(self, share):
        bucket = self.find_bucket(share.space_id)
        if not bucket:
            return None
        key = str(share.id) + '.jpg'

        try:
            self.s3_client.get_object(Bucket=bucket, Key=key)
        except botocore.exceptions.ClientError as ex:
            if ex.response['Error']['Code'] == 'NoSuchKey':
                return None

        return self.s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket, 'Key': key},
            ExpiresIn=3
        )

    def delete_space_directory(self, space):
        bucket = self.find_bucket(space.id)
        if not bucket:
            return

        response = self.s3_client.list_objects_v2(Bucket=bucket)
        if 'Contents' in response:
            objects = response['Contents']
            for obj in objects:
                self.s3_client.delete_object(Bucket=bucket, Key=obj['Key'])

        self.s3_client.delete_bucket(Bucket=bucket)

    def find_bucket(self, space_id):
        for bucket in self.s3_client.list_buckets()['Buckets']:
            if bucket["Name"].startswith('space-id-' + str(space_id)):
                return bucket["Name"]

    def send_file_name_to_sqs(self, file_name):
        boto3.client('sqs', region_name='us-east-1').send_message(
            QueueUrl=self.queue_url,
            MessageBody=file_name,
            MessageGroupId='img',
            MessageDeduplicationId=str(datetime.datetime.now().timestamp())
        )

    def create_temp_directory(self):
        for bucket in self.s3_client.list_buckets()['Buckets']:
            if bucket["Name"] == self.s3_temp_bucket:
                return
        self.s3_client.create_bucket(Bucket=self.s3_temp_bucket)
