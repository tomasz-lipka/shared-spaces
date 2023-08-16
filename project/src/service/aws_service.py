"""
Module containing functionalities related to Amazon Web Services.
"""
import os
import boto3
from flask_login import login_required


S3_BUCKET_NAME = 'shared-spaces-temp'
s3 = boto3.client(
    's3',
    aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
)


@login_required
def upload_image(file, space_id, share_id):
    """
    Upload an image to Amazon S3.
    Args:
        file: The image file to be uploaded.
        space_id (int): ID of the target space.
        share_id (int): ID of the share.
    """
    s3.upload_fileobj(
        file,
        S3_BUCKET_NAME,
        str(space_id) + '-' + str(share_id) + '.jpg'
    )
