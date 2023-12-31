import json
import time
from unittest import TestCase
from test.helper import (
    get_app, create_share, register_and_login, add_member, create_space_as_not_member,
    create_space_as_admin, create_share_with_image, are_images_same
)


class TestGetShares(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = get_app()
        cls.client = cls.app.test_client()

    def test_not_logged_in(self):
        response = self.client.get('/spaces/1/shares')
        self.assertEqual(response.status_code, 401)

    def test_normal_run(self):
        admin_1_token, space_id_1, _ = create_space_as_admin(
            self.client, 'space-1')
        create_share(self.client, space_id_1, admin_1_token)
        member_token, member = register_and_login(self.client)
        admin_2_token, space_id_2, admin_2 = create_space_as_admin(
            self.client, 'space-2')
        _, share_id_2 = create_share(self.client, space_id_2, admin_2_token)
        time.sleep(1)
        add_member(self.client, space_id_2, member.get('login'), admin_2_token)
        _, share_id_3 = create_share(self.client, space_id_2, member_token)

        response = self.client.get(
            f'/spaces/{space_id_2}/shares', headers={"Authorization": f"Bearer {member_token}"})
        expected_data = [
            {
                "id": share_id_3,
                "user": {
                    "id": member.get('id'),
                    "login": member.get('login')
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
        self.assertEqual(response.data, b'Can\'t access this space - not a member')

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
