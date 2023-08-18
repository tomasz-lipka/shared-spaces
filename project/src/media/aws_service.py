import os
import datetime
import boto3
import botocore.exceptions

from ..media.media_service import MediaService


S3_BUCKET = 'shared-spaces-temp'
FILE_FORMAT = '.jpg'
QUEUE_URL = 'https://sqs.us-east-1.amazonaws.com/869305664526/shared-spaces.fifo'
s3_client = boto3.client(
    's3',
    aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
)


class AwsService(MediaService):

    def upload_image(self, file, space_id, share_id):
        object_key = str(space_id) + '-' + str(share_id) + FILE_FORMAT
        s3_client.upload_fileobj(
            file,
            S3_BUCKET,
            object_key
        )
        self.send_file_name_to_sqs(object_key)

    def get_image(self, space_id, share_id):
        bucket = self.find_bucket(space_id)
        if not bucket:
            return None
        key = str(share_id) + '.jpg'

        try:
            s3_client.get_object(Bucket=bucket, Key=key)
        except botocore.exceptions.ClientError as ex:
            if ex.response['Error']['Code'] == 'NoSuchKey':
                return None

        return s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket, 'Key': key},
            ExpiresIn=3
        )

    def delete_space_directory(self, space_id):
        bucket = self.find_bucket(space_id)
        if not bucket:
            return

        response = s3_client.list_objects_v2(Bucket=bucket)
        if 'Contents' in response:
            objects = response['Contents']
            for obj in objects:
                s3_client.delete_object(Bucket=bucket, Key=obj['Key'])

        s3_client.delete_bucket(Bucket=bucket)

    def find_bucket(self, space_id):
        for bucket in s3_client.list_buckets()['Buckets']:
            if bucket["Name"].startswith('space-id-' + str(space_id)):
                return bucket["Name"]

    def send_file_name_to_sqs(self, file_name):
        boto3.client('sqs', region_name='us-east-1').send_message(
            QueueUrl=QUEUE_URL,
            MessageBody=file_name,
            MessageGroupId='img',
            MessageDeduplicationId=str(datetime.datetime.now().timestamp())
        )
