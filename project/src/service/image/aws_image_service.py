"""
Module containing the AWSImageService class.
"""
import os
import datetime
from flask_login import current_user, login_required
import boto3
import botocore.exceptions


from ..image.image_service import ImageService
from ..helper.validator_helper import ValidatorHelper

class AwsImageService(ImageService):
    """
    Concrete implementation of the ImageService abstract class using an AWS client.
    This class provides methods for adding, deleting, and retrieving images 
    to/from AWS and also managing AWS S3 buckets
    """

    FILE_FORMAT = '.jpg'
    MEDIA_URL_EXPIRES_IN = 3

    def __init__(self, queue_url, s3_temp_bucket, mode, validator: ValidatorHelper, ):
        self.queue_url = queue_url
        self.s3_temp_bucket = s3_temp_bucket
        self.mode = mode
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
        )
        self.validator = validator

    @login_required
    def upload_image(self, file, share_id):
        share = self.validator.validate_share(share_id)
        self.validator.validate_share_owner(
            share,
            int(current_user.get_id())
        )

        object_key = str(share.space.id) + '-' + \
            str(share.id) + self.FILE_FORMAT
        self.s3_client.upload_fileobj(
            file,
            self.s3_temp_bucket,
            object_key
        )
        self.__send_file_name_to_sqs(object_key)

    @login_required
    def get_image(self, share):
        bucket = self.__find_bucket(share.space_id)
        if not bucket:
            return None
        key = str(share.id) + self.FILE_FORMAT

        try:
            self.s3_client.get_object(Bucket=bucket, Key=key)
        except botocore.exceptions.ClientError as ex:
            if ex.response['Error']['Code'] == 'NoSuchKey':
                return None

        return self.__generate_presigned_url(bucket, key)

    @login_required
    def delete_space_directory(self, space):
        bucket = self.__find_bucket(space.id)
        if not bucket:
            return
        for obj in self.__get_all_objects(bucket):
            self.s3_client.delete_object(Bucket=bucket, Key=obj['Key'])
        self.s3_client.delete_bucket(Bucket=bucket)

    @login_required
    def get_all_images(self, space_id):
        space = self.validator.validate_space(space_id)
        self.validator.validate_assignment(
            space,
            self.validator.validate_user(current_user.get_id())
        )

        bucket = self.__find_bucket(space.id)
        image_urls = []
        if bucket:
            for obj in self.__get_all_objects(bucket):
                image_urls.append(
                    self.__generate_presigned_url(bucket, obj['Key']))
        return image_urls

    def create_temp_directory(self):
        for bucket in self.s3_client.list_buckets()['Buckets']:
            if bucket["Name"] == self.s3_temp_bucket:
                return
        self.s3_client.create_bucket(Bucket=self.s3_temp_bucket)

    def __find_bucket(self, space_id):
        prefix = 'space-id-'
        if self.mode == 'test':
            prefix = 'test-space-id-'
        for bucket in self.s3_client.list_buckets()['Buckets']:
            if bucket["Name"].startswith(prefix + str(space_id)):
                return bucket["Name"]

    def __send_file_name_to_sqs(self, file_name):
        boto3.client('sqs', region_name='us-east-1').send_message(
            QueueUrl=self.queue_url,
            MessageBody=file_name,
            MessageGroupId=self.mode,
            MessageDeduplicationId=str(datetime.datetime.now().timestamp())
        )

    def __get_all_objects(self, bucket):
        response = self.s3_client.list_objects_v2(Bucket=bucket)
        if 'Contents' in response:
            return response['Contents']

    def __generate_presigned_url(self, bucket, key):
        return self.s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket, 'Key': key},
            ExpiresIn=self.MEDIA_URL_EXPIRES_IN
        )
