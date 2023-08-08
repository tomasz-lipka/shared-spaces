

    def test_add_member_not_exists(self):
        logout()
        register('member')
        login('usr')
        create_space("space-1")

        data = {
            "user-id": "999"
        }
        response = client.post('/spaces/1/members', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"User with ID '999' doesn't exist")

    def test_add_member_to_space_not_exists(self):
        logout()
        register('member')
        login('usr')
        create_space("space-1")

        data = {
            "user-id": "2"
        }
        response = client.post('/spaces/999/members', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Space with ID '999' doesn't exist")
