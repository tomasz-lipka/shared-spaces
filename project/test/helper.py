import time
import boto3
import os
from sqlalchemy import MetaData, Table

from app import create_app

app = create_app('test-app-config.py')
app.config['TESTING'] = True
client = app.test_client()


s3_client = boto3.client(
    's3',
    aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
)


def set_up():
    logout()
    purge_db()


def purge_db():
    metadata = MetaData()
    metadata.reflect(bind=app.engine)

    table_names = metadata.tables.keys()

    with app.engine.begin() as connection:
        for table_name in table_names:
            table = Table(table_name, metadata, autoload=True)
            connection.execute(table.delete())


def register(usr_login):
    data = {
        "login": usr_login,
        "password": "pwd",
        "confirm-password": "pwd"
    }
    return client.post('/register', json=data)


def login(usr_login):
    data = {
        "login": usr_login,
        "password": "pwd"
    }
    return client.post('/login', json=data)


def register_and_login(usr_login):
    register(usr_login)
    return login(usr_login)


def logout():
    client.get('/logout')


def create_space(space_name):
    data = {
        "name": space_name
    }
    return client.post('/spaces', json=data)


def create_space_as_admin(space_name):
    register_and_login('admin')
    return create_space(space_name)


def create_space_as_not_member():
    create_space_as_admin('space-1')
    logout()
    register_and_login('not-member')


def add_member(space_id, user_id):
    data = {
        "user-id": user_id
    }
    return client.post(f'/spaces/{space_id}/members', json=data)


def create_space_as_member(space_name):
    register('member')
    create_space_as_admin(space_name)
    add_member(1, 1)
    logout()
    login('member')


def create_share(space_id):
    data = {
        "text": "Lorem ipsum"
    }
    return client.post(f'/spaces/{space_id}/shares', data=data, content_type='multipart/form-data')


def create_share_with_image(space_id):
    try:
        with open('/workspaces/shared-spaces/project/test/test-image.jpg', 'rb') as image_file:
            data = {
                'text': "Lorem ipsum",
                'file': (image_file, 'test-image.jpg')
            }
            response = client.post(
                f'/spaces/{space_id}/shares',
                data=data,
                content_type='multipart/form-data'
            )
            time.sleep(1)
            return response
    except FileNotFoundError:
        print("Image file not found.")


def delete_all_buckets():
    while __is_only_temp_bucket():
        for bucket in s3_client.list_buckets()['Buckets']:
            if bucket["Name"].startswith('space-id-'):
                __delete_objects_from_bucket(bucket)
                s3_client.delete_bucket(Bucket=bucket["Name"])
        print('try delete all buckets again')


def find_bucket(bucket_name):
    for bucket in s3_client.list_buckets()['Buckets']:
        if bucket["Name"].startswith(bucket_name):
            return True
    return False


def __is_only_temp_bucket():
    return len(s3_client.list_buckets()['Buckets']) > 1


def __delete_objects_from_bucket(bucket):
    response = s3_client.list_objects_v2(Bucket=bucket["Name"])
    if 'Contents' in response:
        objects = response['Contents']
        for obj in objects:
            s3_client.delete_object(
                Bucket=bucket["Name"], Key=obj['Key'])
