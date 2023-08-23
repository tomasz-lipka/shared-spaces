from unittest import TestCase
from test.helper import (
    set_up, client, create_space_as_admin, register_and_login,
    create_share, create_space_as_not_member, create_share_with_image,
    delete_all_buckets, find_bucket
)


class TestCreateShare(TestCase):

    def setUp(self):
        set_up()

    def test_not_logged_in(self):
        response = create_share(1)
        self.assertEqual(response.status_code, 401)

    def test_normal_run(self):
        create_space_as_admin('space-1')
        response = create_share(1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Share created")

    def test_space_not_exist(self):
        register_and_login('admin')
        response = create_share(999)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Space with ID '999' doesn't exist")

    def test_not_member(self):
        create_space_as_not_member()
        response = create_share(1)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b'User-space pair doesn\'t exist')

    def test_wrong_json_key(self):
        create_space_as_admin('space-1')
        data = {
            "wrong": "Lorem ipsum"
        }
        response = client.post('/spaces/1/shares', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Invalid payload: 'text'")

    def test_normal_run_with_image(self):
        create_space_as_admin('space-1')
        response = create_share_with_image(1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Share with image created")

        delete_all_buckets()

    def test_not_logged_in_with_image(self):
        response = create_share_with_image(1)
        self.assertEqual(response.status_code, 401)
        self.assertFalse(find_bucket('space-id-1'))

    def test_space_not_exist_with_image(self):
        register_and_login('admin')
        response = create_share_with_image(999)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Space with ID '999' doesn't exist")
        self.assertFalse(find_bucket('space-id-999'))

    def test_not_member_with_image(self):
        create_space_as_not_member()
        response = create_share_with_image(1)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b'User-space pair doesn\'t exist')
        self.assertFalse(find_bucket('space-id-1'))
