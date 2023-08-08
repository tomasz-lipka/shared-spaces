import json
from unittest import TestCase
from test.helper import register_and_login, create_space, delete_all_records_from_db, client, create_space_by_other_user


class TestAssignmentController(TestCase):

    def setUp(self):
        delete_all_records_from_db()

    def test_get_all_my_spaces(self):
        create_space_by_other_user("space-1")

        register_and_login("this-usr")
        create_space("space-2")
        create_space("space-3")
        response = client.get('/spaces')
        expected_data = [
            {
                "is_admin": True,
                "space": {
                    "id": 2,
                    "name": "space-2"
                }
            },
            {
                "is_admin": True,
                "space": {
                    "id": 3,
                    "name": "space-3"
                }
            }
        ]
        data = json.loads(response.data)
        self.assertEqual(data, expected_data)
        self.assertEqual(response.status_code, 200)


  

    # def add_member_to_space(self):

    # def get_members_of_space(self)

    # def delete_member_from_space(self)

    
    # def test_add_member_to_space_where_only_member(self):

    # def test_get_members_of_space_where_not_member(self)


    

    # def test_rename_space_where_only_member(self)


    # def test_make_member_admin(self)

    # def test_make_admin_member(self)

    
    # def test_make_member_admin_when_only_member(self)

    # def test_make_admin_member_when_only_member(self)


    # def test_delete_not_empty_space(self)
