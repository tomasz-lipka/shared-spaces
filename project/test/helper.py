from io import BytesIO
import os
import time
import json
import boto3
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


def generate_login_from_timestamp():
    timestamp = str(time.time())
    timestamp_without_decimal = timestamp.replace(".", "")
    return timestamp_without_decimal[-15:]


def register(client):
    data = {
        "login": generate_login_from_timestamp(),
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


def register_and_login(client):
    user = register(client)
    token = login(client, user.get('login'))
    return token, user


def create_space(client, space_name, token):
    data = {
        "name": space_name
    }
    response = client.post(
        '/spaces', headers={"Authorization": f"Bearer {token}"}, json=data)
    space_id = json.loads(response.data).get('id', None)
    return response, space_id


def create_space_as_admin(client, space_name):
    token, admin = register_and_login(client)
    _, space_id = create_space(client, space_name, token)
    return token, space_id, admin


def create_space_as_not_member(client):
    _, space_id, _ = create_space_as_admin(client, 'space-1')
    token, _ = register_and_login(client)
    return token, space_id


def add_member(client, space_id, member_login, token):
    data = {
        "login": member_login
    }
    return client.post(f'/spaces/{space_id}/members',
                       json=data, headers={"Authorization": f"Bearer {token}"})


def create_space_as_member(client, space_name):
    member = register(client)
    token, space_id, _ = create_space_as_admin(client, space_name)
    add_member(client, space_id, member.get('login'), token)
    token = login(client, member.get('login'))
    return token, space_id


def create_share(client, space_id, token):
    data = {
        "text": "Lorem ipsum"
    }
    response = client.post(f'/spaces/{space_id}/shares',
                           data=data,
                           content_type='multipart/form-data',
                           headers={"Authorization": f"Bearer {token}"})
    share_id = None
    if response.status_code == 200:
        share_id = json.loads(response.data).get('id')
    return response, share_id


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
        share_id = None
        if response.status_code == 200:
            share_id = json.loads(response.data).get('id')
        return response, share_id


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
