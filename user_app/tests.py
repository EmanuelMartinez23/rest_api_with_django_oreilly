
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK
from rest_framework.test import APITestCase

class RegisterTestCase(APITestCase):
    def test_register(self):
        data = {
            "username": "emanuel",
            "email": "admi@ad.com",
            "password" : "12345",
            "password2": "12345"
        }
        response =  self.client.post(reverse('register'), data)
        self.assertEquals(response.status_code, HTTP_201_CREATED)

class LoginLogoutTestCase(APITestCase):
    # user for test, tempo
    def setUp(self):
        self.user = User.objects.create_user(username = "emanuel", password ="1234")

    def test_login(self):
        data = {
            "username" :"emanuel",
            "password" : "1234"
        }

        response = self.client.post(reverse('login'), data)
        self.assertEquals(response.status_code, HTTP_200_OK)

    def test_logout(self):
        # obtenemos token para enviarloos en los headers para el logout
        self.token = Token.objects.get(user__username = "emanuel")
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + self.token.key)
        response = self.client.post(reverse('logout'))
        self.assertEquals(response.status_code, HTTP_200_OK)