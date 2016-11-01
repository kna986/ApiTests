import unittest
from api_model import ApiModel

class APITestCase(unittest.TestCase):
    '''
    Tests with api calls
    Steps:
    1. Before test: initialization class APIModel and user registration
    2. Trying to obtain information about the user and check the response code
    3. Check the number of fields the user
    4. Check the correct username
    5. Validation of user roles
    6. Trying to check the user's authorization and the response code
    '''


    user_passwd = u'some password'
    user_mail = u'some e-mail'
    user_name = u'Test User'
    user_role = [u'DbRoleCustomer']
    user_id = ApiModel().registers_user(user_mail, user_passwd, user_name)


    def setUp(self):
        self.api = ApiModel()


    def tearDown(self):
        '''
        After Tests - Need DBQuery or API-call for delete test-user.
        Or in tests we need random generate user accountId, but this is bad way
        '''
        pass
        
    def test_get_user(self, ui=user_id):
        self.api.get_user(ui)

    def test_for_numbers_response_fields(self, ui=user_id, un=user_name, ur=user_role):
        about_user = self.api.get_user(ui)
        expected_info = {u'about': u'', u'fullName': un, u'creationTime': u'2016-10-31T11:54:18.902Z', u'id': u'', u'accountId': u'', u'roles': ur}
        for key in expected_info:
            if expected_info[key] > about_user[key]:
                raise AssertionError(key)

    def test_for_value_user_name(self, ui=user_id):
        about_user = self.api.get_user(ui)
        assert about_user.get(u'fullName') == self.user_name

    def test_for_value_user_role(self, ui=user_id):
        about_user = self.api.get_user(ui)
        assert about_user.get(u'roles') == self.user_role

    def test_authorizes_user(self):
        self.api.authorizes_user(self.user_mail, self.user_passwd)


if __name__ == "__main__":
    unittest.main()

