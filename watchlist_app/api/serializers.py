from rest_framework import serializers
from watchlist_app.models import Movie

# Serializador para el modelo Movie
class MovieSerializer(serializers.Serializer):
    # solo vamos a leer 
    id = serializers.IntegerField(read_only = True)
    name = serializers.CharField()
    description = serializers.CharField()
    activate = serializers.BooleanField()

    # metodos para las solicitudes POST para crear un object
    def create(self, validated_data):
        return Movie.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.activate = validated_data.get('activate', instance.activate)
        instance.save()
        return instance
