from rest_framework.test import APITestCase, APIClient


class UserTestCase(APITestCase):
    """Create a user and test API"""

    def setUp(self):
        self.base_url = '/api/users/'
        self.client = APIClient()
        self.user_data = {'username': 'test',
                          'password': 'te123456',
                          'email': 'test@gmail.com',
                          'first_name': 'test',
                          'last_name': 'test', }

        self.signup()

    def signup(self):
        response = self.client.post(self.base_url + 'signup/', data=self.user_data, format='json')
        self.assertTrue(response.status_code // 100 == 2, "Registration failed: " + str(response.status_code))

    def login(self):
        user_credentials = {'username': self.user_data['username'], 'password': self.user_data['password']}
        response = self.client.post(self.base_url + 'login/', data=user_credentials, format='json')
        self.assertTrue(response.status_code // 100 == 2, "login failed: " + str(response.status_code))
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['access'])
        return response.data

    def test_logout(self):
        refresh = self.login()['refresh']
        response = self.client.post(self.base_url + 'logout/', {'refresh': refresh}, format='json')
        self.assertTrue(response.status_code // 100 == 2, "logout failed: " + str(response.status_code))

    def test_reset_password(self):
        self.login()
        data = {'old_password': self.user_data['password'], 'new_password': 'st123456'}
        response = self.client.post(self.base_url + 'change_password/', data=data, format='json')
        self.assertTrue(response.status_code // 100 == 2, "reset password failed: " + str(response.status_code))
        self.client.credentials()

    def test_put_user(self):
        self.login()
        data = {'first_name': "test2", 'last_name': "test2"}
        response = self.client.patch(self.base_url + self.user_data['username'] + '/', data=data)
        self.assertTrue(response.status_code // 100 == 2, "put user failed: " + str(response.status_code))
        self.client.credentials()

    def test_get_user(self):
        response = self.client.get(self.base_url + self.user_data['username'] + '/')
        self.assertTrue(response.status_code // 100 == 2, "get user failed: " + str(response.status_code))

    def test_delete_account(self):
        self.login()
        response = self.client.delete(self.base_url + self.user_data['username'] + '/')
        self.assertTrue(response.status_code // 100 == 2, "delete account failed: " + str(response.status_code))
