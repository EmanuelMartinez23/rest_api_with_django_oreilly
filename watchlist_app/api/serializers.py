from rest_framework import serializers

# Serializador para el modelo Movie
class MovieSerializer(serializers.Serializer):
    # solo vamos a leer 
    id = serializers.IntegerField(read_only = True)
    name = serializers.CharField()
    description = serializers.CharField()
    activate = serializers.BooleanField()
