from django.shortcuts import render
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework_simplejwt.tokens import RefreshToken

from .api.serializer import RegistrationSerializer
from user_app import models

@api_view(['POST',])
def logout_view(request):
    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response(status = HTTP_200_OK)

# creamos la view para registrar el usuario
@api_view(['POST',])
def registration_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data = request.data)
        data = {}
        if serializer.is_valid():
            # guardamoss la cuenta que se registro
            account = serializer.save()
            # almacenamos los valores
            data['response'] = "Registration Successful!"
            data['username']  = account.username
            data['email'] = account.email
            #
            # token = Token.objects.get(user = account).key
            # data['token'] = token
            # creamos r token para user
            refresh = RefreshToken.for_user(account)

            data['token'] = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }

        else:
            data = serializer.errors

        return Response(data)