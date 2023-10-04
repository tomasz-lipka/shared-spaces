from io import BytesIO
import os
import time
import json
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

WRONG_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5NDE2NDIwMSwianRpIjoiNjc0NmNhZGEtNzFjYS00ZGZhLWFkYTUtOTFhYTRlODg2YzZmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InRvbSIsIm5iZiI6MTY5NDE2NDIwMSwiZXhwIjoxNjk0MTY1MTAxfQ.GPN8b1ahikw28Iy8cv3zr3gv_MqHfxZktU5zWEiFGT8"
RESOURCES = '/test/resources/'


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
    response = client.post('/register', json=data)
    user = None
    if response.status_code == 200:
        user = json.loads(response.data.decode('utf-8'))
    return user


def login(client, usr_login):
    data = {
        "login": usr_login,
        "password": "pwd"
    }
    response = client.post('/login', json=data)
    return json.loads(response.data.decode('utf-8')).get('access_token')


def register_and_login(client, usr_login):
    register(client, usr_login)
    return login(client, usr_login)


def logout(client):
    client.delete('/logout')


def create_space(client, space_name, token):
    data = {
        "name": space_name
    }
    response = client.post(
        '/spaces', headers={"Authorization": f"Bearer {token}"}, json=data)
    space_id = json.loads(response.data).get('id', None)
    return response, space_id


def create_space_as_admin(client, space_name):
    token = register_and_login(client, 'admin')
    response, space_id = create_space(client, space_name, token)
    return token, space_id


def create_space_as_not_member(client):
    token, space_id = create_space_as_admin(client, 'space-1')
    logout(client)
    token = register_and_login(client, 'not-member')
    return token, space_id


def add_member(client, space_id, member_login, token):
    data = {
        "login": member_login
    }
    return client.post(f'/spaces/{space_id}/members', json=data, headers={"Authorization": f"Bearer {token}"})


def create_space_as_member(client, space_name):
    register(client, 'member')
    token, space_id = create_space_as_admin(client, space_name)
    add_member(client, 1, 'member', token)
    logout(client)
    token = login(client, 'member')
    return token, space_id


def create_share(client, space_id, token):
    data = {
        "text": "Lorem ipsum"
    }
    return client.post(f'/spaces/{space_id}/shares', data=data, content_type='multipart/form-data', headers={"Authorization": f"Bearer {token}"})


def create_share_with_image(client, space_id, img_name, token):
    image_url = os.getcwd() + RESOURCES + img_name
    with open(image_url, 'rb') as image_file:
        data = {
            'text': "Lorem ipsum",
            'file': (image_file, 'img')
        }
        response = client.post(
            f'/spaces/{space_id}/shares',
            headers={"Authorization": f"Bearer {token}"},
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


def are_images_same(data, test_img_name):
    response = requests.get(data["image_url"])
    image_bytes = BytesIO(response.content)
    image_url = os.getcwd() + RESOURCES + test_img_name

    return not ImageChops.difference(Image.open(image_url), Image.open(image_bytes)).getbbox()


def edit_share_with_image(client, share_id, new_img_name, token):
    image_url = os.getcwd() + RESOURCES + new_img_name
    with open(image_url, 'rb') as image_file:
        data = {
            'text': "Edit lorem ipsum",
            'file': (image_file, 'img')
        }
        response = client.put(
            f'/shares/{share_id}',
            data=data,
            content_type='multipart/form-data',
            headers={"Authorization": f"Bearer {token}"}
        )
        time.sleep(1)
        return response
