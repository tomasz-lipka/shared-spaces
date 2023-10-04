import json
from unittest import TestCase
from test.helper import (
    get_app, logout, purge_db, create_space_as_admin,
    create_share, register_and_login, create_share_with_image,
    create_space, register, login, add_member, find_bucket, are_images_same,
    WRONG_TOKEN
)


class TestGetShare(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = get_app()
        cls.client = cls.app.test_client()

    def setUp(self):
        logout(self.client)
        purge_db(self.app)

    def test_not_logged_in(self):
        response = self.client.get(
            '/shares/1', headers={"Authorization": f"Bearer {WRONG_TOKEN}"})
        self.assertEqual(
            response.data, b'{"msg":"Signature verification failed"}\n')
        self.assertEqual(response.status_code, 422)

    def test_normal_run(self):
        token, space_id, admin = create_space_as_admin(self.client, 'space-1')
        _, share_id = create_share(self.client, 1, token)
        response = self.client.get(
            f'/shares/{share_id}', headers={"Authorization": f"Bearer {token}"})
        expected_data = {
            "id": share_id,
            "space": {
                "id": space_id,
                "name": "space-1"
            },
            "user": {
                "id": admin.get('id'),
                "login": admin.get('login')
            },
            "text": "Lorem ipsum",
            # "timestamp":
            "image_url": None
        }
        data = json.loads(response.data)
        data.pop("timestamp", None)
        self.assertEqual(data, expected_data)
        self.assertEqual(response.status_code, 200)

    def test_not_exist(self):
        token, _ = register_and_login(self.client)
        response = self.client.get(
            '/shares/999999999', headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, b'No such share')

    def test_not_owned(self):
        token, _, _ = create_space_as_admin(self.client, 'space-1')
        _, share_id = create_share(self.client, 1, token)
        logout(self.client)
        token, _ = register_and_login(self.client)
        response = self.client.get(
            f'/shares/{share_id}', headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, b'User doesn\'t own this share')

    def test_normal_run_with_image(self):
        token, space_id_1, admin = create_space_as_admin(
            self.client, 'space-1')
        create_share_with_image(
            self.client, 1, 'test-image-1.jpg', token)
        _, space_id_2 = create_space(self.client, 'space-2', token)
        logout(self.client)
        user = register(self.client)
        token = login(self.client, admin.get('login'))
        add_member(self.client, space_id_2, user.get('login'), token)
        logout(self.client)
        token = login(self.client, user.get('login'))
        create_share_with_image(
            self.client, space_id_2, 'test-image-2.jpg', token)
        _, share_id_3 = create_share_with_image(
            self.client, space_id_2, 'test-image-3.jpg', token)

        response = self.client.get(
            f'/shares/{share_id_3}', headers={"Authorization": f"Bearer {token}"})
        expected_data = {
            "id": share_id_3,
            "space": {
                "id": space_id_2,
                "name": "space-2"
            },
            "user": {
                "id": user.get('id'),
                "login": user.get('login')
            },
            "text": "Lorem ipsum"
            # "timestamp":
            # "image_url":
        }
        data = json.loads(response.data)

        self.assertTrue(are_images_same(
            data, 'test-image-3.jpg'))

        data.pop("timestamp", None)
        data.pop("image_url", None)
        self.assertEqual(data, expected_data)
        self.assertEqual(response.status_code, 200)

        logout(self.client)
        token = login(self.client, admin.get('login'))
        self.client.delete(f'/spaces/{space_id_2}/members/{user.get("id")}',
                           headers={"Authorization": f"Bearer {token}"})
        self.client.delete(
            f'/spaces/{space_id_1}', headers={"Authorization": f"Bearer {token}"})
        self.client.delete(
            f'/spaces/{space_id_2}', headers={"Authorization": f"Bearer {token}"})

    def test_not_owned_with_image(self):
        token, space_id, admin = create_space_as_admin(self.client, 'space-1')
        _, share_id = create_share_with_image(
            self.client, 1, 'test-image-1.jpg', token)
        logout(self.client)
        token, _ = register_and_login(self.client)
        response = self.client.get(
            f'/shares/{share_id}', headers={"Authorization": f"Bearer {token}"})

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, b'User doesn\'t own this share')
        self.assertTrue(find_bucket(f'test-space-id-{space_id}'))

        logout(self.client)
        token = login(self.client, admin.get('login'))
        self.client.delete(
            f'/spaces/{space_id}', headers={"Authorization": f"Bearer {token}"})
