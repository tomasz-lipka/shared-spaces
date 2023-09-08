from unittest import TestCase
from test.helper import (
    get_app, logout, purge_db, create_space_as_admin, register_and_login,
    create_share, create_space_as_not_member, create_share_with_image,
    find_bucket
)


class TestCreateShare(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = get_app()
        cls.client = cls.app.test_client()

    def setUp(self):
        logout(self.client)
        purge_db(self.app)

    def test_not_logged_in(self):
        response = create_share(self.client, 1, "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5NDE2NDIwMSwianRpIjoiNjc0NmNhZGEtNzFjYS00ZGZhLWFkYTUtOTFhYTRlODg2YzZmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InRvbSIsIm5iZiI6MTY5NDE2NDIwMSwiZXhwIjoxNjk0MTY1MTAxfQ.GPN8b1ahikw28Iy8cv3zr3gv_MqHfxZktU5zWEiFGT8")
        self.assertEqual(
            response.data, b'{"msg":"Signature verification failed"}\n')
        self.assertEqual(response.status_code, 422)

    def test_normal_run(self):
        token = create_space_as_admin(self.client, 'space-1')
        response = create_share(self.client, 1, token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Share created")

    def test_space_not_exist(self):
        token = register_and_login(self.client, 'admin')
        response = create_share(self.client, 999, token)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, b"Space with ID '999' doesn't exist")

    def test_not_member(self):
        token = create_space_as_not_member(self.client)
        response = create_share(self.client, 1, token)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, b'User-space pair doesn\'t exist')

    def test_wrong_json_key(self):
        token = create_space_as_admin(self.client, 'space-1')
        data = {
            "wrong": "Lorem ipsum"
        }
        response = self.client.post(
            '/spaces/1/shares', data=data, headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Text must be provided")

    def test_normal_run_with_image(self):
        token = create_space_as_admin(self.client, 'space-1')
        response = create_share_with_image(
            self.client, 1, '/workspaces/shared-spaces/project/test/resources/test-image-1.jpg', token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Share with image created")
        self.client.delete('/spaces/1')

    def test_not_logged_in_with_image(self):
        token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5NDE2NDIwMSwianRpIjoiNjc0NmNhZGEtNzFjYS00ZGZhLWFkYTUtOTFhYTRlODg2YzZmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InRvbSIsIm5iZiI6MTY5NDE2NDIwMSwiZXhwIjoxNjk0MTY1MTAxfQ.GPN8b1ahikw28Iy8cv3zr3gv_MqHfxZktU5zWEiFGT8"
        response = create_share_with_image(
            self.client, 1, '/workspaces/shared-spaces/project/test/resources/test-image-1.jpg', token)
        self.assertEqual(
            response.data, b'{"msg":"Signature verification failed"}\n')
        self.assertEqual(response.status_code, 422)
        self.assertFalse(find_bucket('test-space-id-1'))

    def test_space_not_exist_with_image(self):
        token = register_and_login(self.client, 'admin')
        response = create_share_with_image(
            self.client, 999, '/workspaces/shared-spaces/project/test/resources/test-image-1.jpg', token)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, b"Space with ID '999' doesn't exist")
        self.assertFalse(find_bucket('test-space-id-999'))

    def test_not_member_with_image(self):
        token = create_space_as_not_member(self.client)
        response = create_share_with_image(
            self.client, 1, '/workspaces/shared-spaces/project/test/resources/test-image-1.jpg', token)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, b'User-space pair doesn\'t exist')
        self.assertFalse(find_bucket('test-space-id-1'))

    def test_null_json_value(self):
        token = create_space_as_admin(self.client, 'space-1')
        data = {
            "text": None
        }
        response = self.client.post(
            '/spaces/1/shares', data=data, headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Text must be provided")

    def test_empty_text(self):
        token = create_space_as_admin(self.client, 'space-1')
        data = {
            "text": "    "
        }
        response = self.client.post(
            '/spaces/1/shares', data=data, headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Text cannot be empty")

    def test_min_char_text(self):
        token = create_space_as_admin(self.client, 'space-1')
        data = {
            "text": "a"
        }
        response = self.client.post(
            '/spaces/1/shares', data=data, headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Text min 3 characters")

    def test_max_char_text(self):
        token = create_space_as_admin(self.client, 'space-1')
        data = {
            "text": "text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text text "
        }
        response = self.client.post(
            '/spaces/1/shares', data=data, headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Text max 200 characters")
