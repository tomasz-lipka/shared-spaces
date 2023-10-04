import json
import time
from unittest import TestCase
from test.helper import (
    get_app, logout, purge_db, create_share, register_and_login, create_space,
    register, add_member, login, create_space_as_not_member,
    create_space_as_admin, create_share_with_image, are_images_same
)


class TestGetShares(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = get_app()
        cls.client = cls.app.test_client()

    def setUp(self):
        logout(self.client)
        purge_db(self.app)

    def test_not_logged_in(self):
        response = self.client.get('/spaces/1/shares')
        self.assertEqual(response.status_code, 401)

    def test_normal_run(self):
        token, _ = register_and_login(self.client)
        _, space_id_1 = create_space(self.client, 'space-1', token)
        create_share(self.client, space_id_1, token)
        logout(self.client)

        member_1 = register(self.client)

        token, admin_2 = register_and_login(self.client)
        _, space_id_2 = create_space(self.client, 'space-2', token)
        _, share_id_2 = create_share(self.client, space_id_2, token)
        time.sleep(0.5)
        add_member(self.client, space_id_2, member_1.get('login'), token)
        logout(self.client)

        token = login(self.client, member_1.get('login'))
        _, share_id_3 = create_share(self.client, space_id_2, token)

        response = self.client.get(
            f'/spaces/{space_id_2}/shares', headers={"Authorization": f"Bearer {token}"})
        expected_data = [
            {
                "id": share_id_3,
                "user": {
                    "id": member_1.get('id'),
                    "login": member_1.get('login')
                },
                "text": "Lorem ipsum",
                # "timestamp":
                "image_url": None
            },
            {
                "id": share_id_2,
                "user": {
                    "id": admin_2.get('id'),
                    "login": admin_2.get('login')
                },
                "text": "Lorem ipsum",
                # "timestamp":
                "image_url": None
            }
        ]
        data = json.loads(response.data)
        for item in data:
            item.pop("timestamp", None)
        self.assertEqual(data, expected_data)
        self.assertEqual(response.status_code, 200)

    def test_space_not_exist(self):
        token, _ = register_and_login(self.client)
        response = self.client.get(
            '/spaces/999999999/shares', headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.data, b"Space with ID '999999999' doesn't exist")

    def test_not_member(self):
        token, space_id = create_space_as_not_member(self.client)
        response = self.client.get(
            f'/spaces/{space_id}/shares', headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, b'User-space pair doesn\'t exist')

    def test_normal_run_with_image(self):
        token, space_id, admin = create_space_as_admin(self.client, 'space-1')
        _, share_id_1 = create_share_with_image(
            self.client, space_id, 'test-image-1.jpg', token)
        time.sleep(0.5)
        _, share_id_2 = create_share_with_image(
            self.client, space_id, 'test-image-2.jpg', token)
        time.sleep(0.5)
        _, share_id_3 = create_share(self.client, space_id, token)
        time.sleep(0.5)

        response = self.client.get(
            f'/spaces/{space_id}/shares', headers={"Authorization": f"Bearer {token}"})
        expected_data = [
            {
                "id": share_id_3,
                "user": {
                    "id": admin.get('id'),
                    "login": admin.get('login')
                },
                "text": "Lorem ipsum",
                # "timestamp":
                "image_url": None
            },
            {
                "id": share_id_2,
                "user": {
                    "id": admin.get('id'),
                    "login": admin.get('login')
                },
                "text": "Lorem ipsum",
                # "timestamp":
                # "image_url":
            },
            {
                "id": share_id_1,
                "user": {
                    "id": admin.get('id'),
                    "login": admin.get('login')
                },
                "text": "Lorem ipsum",
                # "timestamp":
                # "image_url":
            }
        ]
        data = json.loads(response.data)

        self.assertTrue(are_images_same(
            data[2], 'test-image-1.jpg'))

        self.assertTrue(are_images_same(
            data[1], 'test-image-2.jpg'))

        data[1].pop("image_url", None)
        data[2].pop("image_url", None)
        for item in data:
            item.pop("timestamp", None)
        self.assertEqual(data, expected_data)
        self.assertEqual(response.status_code, 200)

        self.client.delete(
            f'/spaces/{space_id}', headers={"Authorization": f"Bearer {token}"})
