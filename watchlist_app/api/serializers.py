from rest_framework import serializers
from ..models import WatchList, StreamPlatform


#
# def name_length(value):
#     if len(value) < 2 :
#         raise serializers.ValidationError("Name is too short!")
#
#
# # Serializador para el modelo Movie
# class MovieSerializer(serializers.Serializer):
#     # solo vamos a leer
#     id = serializers.IntegerField(read_only = True)
#     name = serializers.CharField(validators=[name_length])
#     description = serializers.CharField()
#     activate = serializers.BooleanField()
#
#     # metodos para las solicitudes POST para crear un object
#     def create(self, validated_data):
#         return Movie.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get('description', instance.description)
#         instance.activate = validated_data.get('activate', instance.activate)
#         instance.save()
#         return instance
#
#     # field-level validation
#     # validacion del campo name
#     # def validate_name(self, value):
#     #     if len(value) < 2:
#     #         raise serializers.ValidationError("Name is too short!")
#     #     else:
#     #         return value
#
#     # object-level validation
#     # validamos si el objeto tiene el mismo titulo y descripción
#     def validate(self, data):
#         if data['name'] == data['description']:
#             raise serializers.ValidationError("Title and description should be different!")
#         else:
#             return data
#
#



### Serializer with ModelSerializer
class WatchListSerializer(serializers.ModelSerializer):
    # Creamos un field personalizado
    # len_name = serializers.SerializerMethodField()

    class Meta:
        model  = WatchList
        fields = "__all__" # todos los campos del modelo


## Serializer with ModelSerializer
class StreamPlatformSerializer (serializers.ModelSerializer):
    # Create relationship in Serializer
    watchlist = WatchListSerializer(many=True, read_only=True)

    class Meta:
        model = StreamPlatform
        fields  ="__all__"
