import json
from unittest import TestCase
from test.helper import (
    get_app, create_space_as_admin,
    create_share, register_and_login, create_share_with_image,
    create_space, add_member, find_bucket, are_images_same,
    WRONG_TOKEN
)


class TestGetShare(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = get_app()
        cls.client = cls.app.test_client()

    def test_not_logged_in(self):
        response = self.client.get(
            '/shares/1', headers={"Authorization": f"Bearer {WRONG_TOKEN}"})
        self.assertEqual(
            response.data, b'{"msg":"Signature verification failed"}\n')
        self.assertEqual(response.status_code, 422)

    def test_normal_run(self):
        token, space_id, admin = create_space_as_admin(self.client, 'space-1')
        _, share_id = create_share(self.client, space_id, token)
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
        admin_token, space_id, _ = create_space_as_admin(
            self.client, 'space-1')
        _, share_id = create_share(self.client, space_id, admin_token)
        not_owner_token, _ = register_and_login(self.client)
        response = self.client.get(
            f'/shares/{share_id}', headers={"Authorization": f"Bearer {not_owner_token}"})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, b'User doesn\'t own this share')

    def test_normal_run_with_image(self):
        admin_token, space_id_1, _ = create_space_as_admin(
            self.client, 'space-1')
        create_share_with_image(
            self.client, space_id_1, 'test-image-1.jpg', admin_token)
        _, space_id_2 = create_space(self.client, 'space-2', admin_token)
        user_token, user = register_and_login(self.client)
        add_member(self.client, space_id_2, user.get('login'), admin_token)
        create_share_with_image(
            self.client, space_id_2, 'test-image-2.jpg', user_token)
        _, share_id_3 = create_share_with_image(
            self.client, space_id_2, 'test-image-3.jpg', user_token)

        response = self.client.get(
            f'/shares/{share_id_3}', headers={"Authorization": f"Bearer {user_token}"})
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

        self.client.delete(f'/spaces/{space_id_2}/members/{user.get("id")}',
                           headers={"Authorization": f"Bearer {admin_token}"})
        self.client.delete(
            f'/spaces/{space_id_1}', headers={"Authorization": f"Bearer {admin_token}"})
        self.client.delete(
            f'/spaces/{space_id_2}', headers={"Authorization": f"Bearer {admin_token}"})

    def test_not_owned_with_image(self):
        admin_token, space_id, _ = create_space_as_admin(
            self.client, 'space-1')
        _, share_id = create_share_with_image(
            self.client, space_id, 'test-image-1.jpg', admin_token)
        not_owner_token, _ = register_and_login(self.client)
        response = self.client.get(
            f'/shares/{share_id}', headers={"Authorization": f"Bearer {not_owner_token}"})

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, b'User doesn\'t own this share')
        self.assertTrue(find_bucket(f'test-space-id-{space_id}'))

        self.client.delete(
            f'/spaces/{space_id}', headers={"Authorization": f"Bearer {admin_token}"})
