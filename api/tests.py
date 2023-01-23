from api.models import MyUser
from rest_framework.test import RequestsClient, APITestCase


# tests login and register
class LoginTestCase(APITestCase):
    def setUp(self):
        user = MyUser(
            email='testing@login.com',
            first_name='Testing',
            last_name='Testing',
            username='testing_login'
        )
        user.set_password('goodPassword')
        user.save()

    def test_user_login(self):
        """Check if the user can login and get de access token. endpoint: '/api/login'"""

        response = self.client.post('http://testserver/api/login', {
            "email": "testing@login.com",
            "password": "goodPassword"
        },
        format='json')
        assert response.status_code == 200
        assert 'token' in response.json()

    def test_user_login_not_found(self):
        """Check if a wrong email returns 404. endpoint: '/api/login'"""

        response = self.client.post('http://testserver/api/login', {
            "email": "testing@notfound.com",
            "password": "goodPassword"
        },
        format='json')
        assert response.status_code == 404

    def test_user_login_bad_password(self):
        """Check if a wrong password returns 401. endpoint: '/api/login'"""

        response = self.client.post('http://testserver/api/login', {
            "email": "testing@login.com",
            "password": "badPassword"
        },
        format='json')
        assert response.status_code == 401


    def test_user_register(self):
        """Check if the user can register and then login succesfully. endpoint: '/api/register'"""

        response = self.client.post('http://testserver/api/register', {
            "email": "testing@register.com",
            "password": "goodPassword"
        },
        format='json')

        assert response.status_code == 201

        users = MyUser.objects.filter(email='testing@register.com')
        assert len(users) == 1

        response = self.client.post('http://testserver/api/login', {
            "email": "testing@register.com",
            "password": "goodPassword"
        },
        format='json')
        assert response.status_code == 200
        assert 'token' in response.json()

