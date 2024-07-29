import json
from rest_framework.test import APITestCase, APIClient


class UserTestCase(APITestCase):
    """Create a user and test API"""

    def test(self):
        self.client = APIClient()
        self.user_data = {'username': 'test10',
                          'password': 'te123456',
                          'email': 'test@gmail.com',
                          'first_name': 'test',
                          'last_name': 'test', }

        response = self.client.post('/users/', data=self.user_data, format='json')
        self.assertTrue(response.status_code // 100 == 2, "Registration failed: " + str(response.status_code))

        self.user_credentials = {'username': self.user_data['username'], 'password': self.user_data['password']}
        response = self.client.post("/login/", data=self.user_credentials, format='json')
        self.assertTrue(response.status_code // 100 == 2, "login failed: " + str(response.status_code))
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['access'])
