from rest_framework import serializers
from rest_framework.relations import StringRelatedField

from ..models import WatchList, StreamPlatform, Review


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


class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only =True)
    class Meta:
        model = Review
        exclude = ('watchlist',)
        # fields = "__all__"

### Serializer with ModelSerializer
class WatchListSerializer(serializers.ModelSerializer):
    # Creamos un field personalizado
    # len_name = serializers.SerializerMethodField()
    reviews = ReviewSerializer(many = True, read_only = True)

    class Meta:
        model  = WatchList
        fields = "__all__" # todos los campos del modelo


## Serializer with ModelSerializer
# Test with HyperLinkModelSerializer, the difference between ModelSerializer and HyperLinkedModelSerializer is
# that HyperLinkenModelSerializer uses Hyperlinks and ModelSerializer uses primary keys.
# class StreamPlatformSerializer (serializers.HyperlinkedModelSerializer):
class StreamPlatformSerializer (serializers.ModelSerializer):
    # Create relationship in Serializer
    watchlist = WatchListSerializer(many=True, read_only=True)
    # Test para serializer relations field
    #watchlist = StringRelatedField(many = True) # get value __str__
    # watchlist = serializers.PrimaryKeyRelatedField(many = True, read_only=True) # get pk model
    # watchlist = serializers.HyperlinkedRelatedField(
    #     many =True,
    #     read_only = True,
    #     view_name= 'watch-list-details'
    # ) # created hyperlink for each object

    class Meta:
        model = StreamPlatform
        fields  ="__all__"
        extra_kwargs = {
            'url': {'view_name': 'stream-detail'}  # Este campo asegura que 'url' use la vista correcta
        }
