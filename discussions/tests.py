from rest_framework.test import APITestCase, APIClient

from accounts.models import User
from .models import Topic, Comment
from rest_framework_simplejwt.tokens import AccessToken


class DiscussionTestCase(APITestCase):
    def setUp(self):
        self.base_url = '/api/topics/'
        self.user = User.objects.create(email='test10@gmail.com', password='te123456', username='test10',
                                        first_name='test', last_name='test')
        self.topic = Topic.objects.create(owner=self.user, title="test", content="test")
        self.comment = Comment.objects.create(owner=self.user, topic=self.topic, content="test")
        self.client = APIClient()

    def login(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(AccessToken.for_user(self.user)))

    def test_topic(self):
        response = self.client.get(self.base_url)
        self.assertTrue(response.status_code // 100 == 2, "Topics listing failed: " + str(response.status_code))

        self.login()
        response = self.client.post(self.base_url, data={'title': 'test2', 'content': 'test'}, format='json')
        self.assertTrue(response.status_code // 100 == 2, "Topic creation failed: " + str(response.status_code))

        response = self.client.patch(self.base_url + str(response.data['id']) + '/',
                                     data={'title': 'test2', 'content': 'test'}, format='json')
        self.assertTrue(response.status_code // 100 == 2, "Topic update failed: " + str(response.status_code))

        response = self.client.get("/api/search/te/")
        self.assertTrue(response.status_code // 100 == 2, "Topics searching failed: " + str(response.status_code))
        print(response.data)

    def test_comment(self):
        response = self.client.get(self.base_url + str(self.topic.pk) + "/comments/")
        self.assertTrue(response.status_code // 100 == 2, "Comment listing failed: " + str(response.status_code))

        self.login()
        response = self.client.post(self.base_url + str(self.topic.pk) + "/comments/",
                                    data={'content': 'test'}, format='json')
        self.assertTrue(response.status_code // 100 == 2, "Comment creation failed: " + str(response.status_code))

        response = self.client.patch(self.base_url + str(self.topic.pk) + "/comments/" + str(response.data['id']) + '/',
                                     data={'content': 'test2'}, format='json')
        self.assertTrue(response.status_code // 100 == 2, "Comment update failed: " + str(response.status_code))
