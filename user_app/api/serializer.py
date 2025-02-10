from django.contrib.auth.models import User
from django.core.serializers import serialize
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style= {'input_type':'password'}, write_only=True)

    # clase donde vamos agregar el modelo a usar y los campos
    class Meta:
        model = User
        fields = ['username','email', 'password','password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    # debemos de sobreescribir el metodo save() del serializador ya que tenemos
    # el nuevo campo de password2
    def save(self, **kwargs):
        # Conseguimos los valores
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise ValidationError({'error': 'P1 and P2 would be same!'})
        # Nos aseguramos que el email sea único
        if User.objects.filter(email = self.validated_data['email']).exists():
            raise ValidationError({'error':'Email already exists!'})

        # si todo va bien guardamos el usuario con lo que mando username, email,password
        # almacenamos
        account = User(email = self.validated_data['email'], username = self.validated_data['username'])
        account.set_password(password)
        account.save()
        return account