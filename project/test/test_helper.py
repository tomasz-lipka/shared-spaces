import os


def register(client):
    data = {
        "login": "test_user",
        "password": "pwd",
        "confirm-password": "pwd"
    }
    client.post('/register', json=data)


def login(client):
    data = {
        "login": "test_user",
        "password": "pwd"
    }
    client.post('/login', json=data)


def register_and_login(client):
    register(client)
    login(client)


def delete_db_file():
    file_path = "/workspaces/shared-spaces/project/my_db.sqlite"
    os.remove(file_path)
