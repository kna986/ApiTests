try:
    import ujson as json
except ImportError:
    import json

import requests

class ApiModel(object):
    '''
    Class for using API calls
    '''

    def __init__(self, addr='https://beta.1neschool.com'):
        '''
        Initialization url, session establishment, update header
        '''
        self.url = addr
        self.s = requests.Session()
        self.s.get(self.url)
        self.s.post(self.url)
        self.s.delete(self.url)
        self.s.headers.update({'content-type': 'application/json'})

    def get_user(self, user_id):
        ''' GET info about user
        Return: dict with user's profile information
        '''
        result = self.s.get(self.url + '/core/users/' + user_id)
        try:
            assert result.status_code == 200
        except AssertionError:
            raise Exception(result.status_code)
        return json.loads(result.text)

    def get_ticket(self, ticket_id):
        ''' GET info about users ticket (only in admin account), and only one ticket
        because, ticket_id is string, not array.
        Return: dict with ticket's information
        '''
        result = self.s.get(self.url + '/tickets/' + ticket_id)
        try:
            assert result.status_code == 200
        except AssertionError:
            raise Exception(result.status_code)
        return json.loads(result.text)

    def registers_user(self, mail, passwd, user_name):
        ''' POST Registers user and sets session cookie. Does not require authorization
        Must have three credentials
        Return: dict with userId: String and sessionId: String
        '''
        data = {"authType": "DbAuthTypeInternal", "authAccountId":mail, "password":passwd, "name": user_name, "remember": False}
        result = self.s.post(self.url + '/core/users', data=json.dumps(data))
        try:
            assert result.status_code == 200
        except AssertionError:
            raise Exception(result.status_code)
        get_dict = json.loads(result.text)
        return get_dict['userId']


    def authorizes_user(self, authAccount_id, password, auth_type=u'Internal'):
        ''' POST authorizes user and sets session cookie
        Return: dict with userId: String and sessionId: String
        '''
        data = {"password":password}
        result = self.s.post(self.url + '/acl/auth/%s/%s' % (auth_type, authAccount_id), data=json.dumps(data))
        try:
            assert result.status_code == 200
        except AssertionError:
            raise Exception(result.status_code)
        return json.loads(result.text)

    def change_user_role(self, user_id, user_role):
        ''' POST Grants specific role to user.
        Return: dict
        '''
        data = {"role":user_role}
        result = self.s.post(self.url + '/acl/users/' + user_id + '/roles', data=json.dumps(data))
        try:
            assert result.status_code == 200
        except AssertionError:
            raise Exception(result.status_code)
        return json.loads(result.text)

    def user_role_delete(self, user_id, role):
        ''' DELETE Grants specific role to user.
        Return: True or False (Exception with response status code)
        '''
        data = {"role":role}
        result = self.s.delete(self.url + '/acl/users/' + user_id + '/roles', data=json.dumps(data))
        try:
            assert result.status_code == 200
        except AssertionError:
            raise Exception(result.status_code)