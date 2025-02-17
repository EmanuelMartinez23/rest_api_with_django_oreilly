from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.status import HTTP_201_CREATED, HTTP_403_FORBIDDEN, HTTP_200_OK
from rest_framework.test import APITestCase
from watchlist_app import models

class StreamPlatformTests(APITestCase):
    # Creamos un usuario y obtenemos el token para las request
    def setUp(self):
        self.user = User.objects.create_user(username = "example", password = "1234" )
        self.token = Token.objects.get(user__username = self.user)
        # añadimos el token en los headers
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # agregar elementos a la tablas
        self.stream = models.StreamPlatform.objects.create(name = "Netflix",
                                                           about = "# the best plataform",
                                                           website = "https://netflix.com")
    # test para crear una platforma
    def test_streamplatform_create(self):
        data = {
            "name" : "Netflix",
            "about" : "The best stream plataform",
            "website": "https://netflix.com"
        }

        response = self.client.post(reverse('stream-list'), data)
        self.assertEquals(response.status_code, HTTP_403_FORBIDDEN)
    # test para listar plataformas
    def test_streamplatform_list(self):
        response = self.client.get(reverse('stream-list'))
        self.assertEquals(response.status_code, HTTP_200_OK)

    # test para una sola plataforma
    def test_streamplatform_id(self):
        response = self.client.get(reverse('stream-detail', args = (self.stream.id,)))
        self.assertEquals(response.status_code, HTTP_200_OK)

