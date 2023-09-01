from io import BytesIO
import os
import time
import boto3
from sqlalchemy import MetaData, Table
from PIL import Image, ImageChops
import requests

from app import create_app


s3_client = boto3.client(
    's3',
    aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
)


def get_app():
    app = create_app('test-app.config')
    app.config['TESTING'] = True
    return app


def purge_db(app):
    metadata = MetaData()
    metadata.reflect(bind=app.engine)

    table_names = metadata.tables.keys()

    with app.engine.begin() as connection:
        for table_name in table_names:
            table = Table(table_name, metadata, autoload=True)
            connection.execute(table.delete())


def register(client, usr_login):
    data = {
        "login": usr_login,
        "password": "pwd",
        "confirm-password": "pwd"
    }
    return client.post('/register', json=data)


def login(client, usr_login):
    data = {
        "login": usr_login,
        "password": "pwd"
    }
    return client.post('/login', json=data)


def register_and_login(client, usr_login):
    register(client, usr_login)
    return login(client, usr_login)


def logout(client):
    client.get('/logout')


def create_space(client, space_name):
    data = {
        "name": space_name
    }
    return client.post('/spaces', json=data)


def create_space_as_admin(client, space_name):
    register_and_login(client, 'admin')
    return create_space(client, space_name)


def create_space_as_not_member(client):
    create_space_as_admin(client, 'space-1')
    logout(client)
    register_and_login(client, 'not-member')


def add_member(client, space_id, user_id):
    data = {
        "user-id": user_id
    }
    return client.post(f'/spaces/{space_id}/members', json=data)


def create_space_as_member(client, space_name):
    register(client, 'member')
    create_space_as_admin(client, space_name)
    add_member(client, 1, 1)
    logout(client)
    login(client, 'member')


def create_share(client, space_id):
    data = {
        "text": "Lorem ipsum"
    }
    return client.post(f'/spaces/{space_id}/shares', data=data, content_type='multipart/form-data')


def create_share_with_image(client, space_id, img_url):
    with open(img_url, 'rb') as image_file:
        data = {
            'text': "Lorem ipsum",
            'file': (image_file, 'img')
        }
        response = client.post(
            f'/spaces/{space_id}/shares',
            data=data,
            content_type='multipart/form-data'
        )
        time.sleep(1)
        return response


def find_bucket(bucket_name):
    for bucket in s3_client.list_buckets()['Buckets']:
        if bucket["Name"].startswith(bucket_name):
            return True
    return False


def are_images_same(data, test_img):
    response = requests.get(data["image_url"])
    image_bytes = BytesIO(response.content)

    return not ImageChops.difference(Image.open(test_img), Image.open(image_bytes)).getbbox()


def edit_share_with_image(client, share_id, new_img_url):
    with open(new_img_url, 'rb') as image_file:
        data = {
            'text': "Edit lorem ipsum",
            'file': (image_file, 'img')
        }
        response = client.put(
            f'/shares/{share_id}',
            data=data,
            content_type='multipart/form-data'
        )
        time.sleep(1)
        return response
