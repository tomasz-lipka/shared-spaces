import json
from unittest import TestCase
from test.helper import register_and_login, get_app, create_space, create_space_as_not_member


class TestGetSpaces(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = get_app()
        cls.client = cls.app.test_client()

    def test_not_logged_in(self):
        response = self.client.get('/spaces')
        self.assertEqual(response.status_code, 401)

    def test_normal_run(self):
        token, _ = register_and_login(self.client)
        response, space_id_1 = create_space(self.client, "B-space", token)
        response, space_id_2 = create_space(self.client, "a-space", token)
        response, space_id_3 = create_space(self.client, "c-space", token)
        response = self.client.get(
            '/spaces', headers={"Authorization": f"Bearer {token}"})
        expected_data = [
            {
                "is_admin": True,
                "space": {
                    "id": space_id_2,
                    "name": "a-space"
                }
            },
            {
                "is_admin": True,
                "space": {
                    "id": space_id_1,
                    "name": "B-space"
                }
            },
            {
                "is_admin": True,
                "space": {
                    "id": space_id_3,
                    "name": "c-space"
                }
            }
        ]
        data = json.loads(response.data)
        self.assertEqual(data, expected_data)
        self.assertEqual(response.status_code, 200)

    def test_not_member(self):
        token, _ = create_space_as_not_member(self.client)
        response, space_id_2 = create_space(self.client, 'space-2', token)
        response = self.client.get(
            '/spaces', headers={"Authorization": f"Bearer {token}"})
        expected_data = [
            {
                "is_admin": True,
                "space": {
                    "id": space_id_2,
                    "name": "space-2"
                }
            }
        ]
        data = json.loads(response.data)
        self.assertEqual(data, expected_data)
        self.assertEqual(response.status_code, 200)
