from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_204_NO_CONTENT
from rest_framework.views import APIView

from .serializers import StreamPlatformSerializer
from ..models import WatchList, StreamPlatform
from ..api.serializers import WatchListSerializer
from rest_framework.response import Response
from rest_framework import status


class StreamListAV(APIView):
    def get(self, request):
        platform = StreamPlatform.objects.all()
        # serializer for HyperLinkRelatedField and HyperLinkedModelSerializer, because need context of request
        serializer = StreamPlatformSerializer(platform,many=True, context={'request': request})
        return Response(serializer.data)
        # serializer = StreamPlatformSerializer(platform,many =True)


    def post(self,request):
        serializer = StreamPlatformSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status = HTTP_400_BAD_REQUEST)



class StreamPlatformDetailAV(APIView):
    def get(self,request,pk):
        try:
            platform = StreamPlatform.objects.get(pk = pk)
        except StreamPlatform.DoesNotExist:
            return Response(
                { "error : Platform not found" },
                status=HTTP_400_BAD_REQUEST
            )

        serializer = StreamPlatformSerializer(platform, context={'request': request})
        return Response(
            serializer.data,
            status= HTTP_200_OK
        )

    def put(self,request,pk):
        try:
            platform = StreamPlatform.objects.get(pk = pk)
        except StreamPlatform.DoesNotExist:
            return Response(
                {"error : Platform not found" },
                status = HTTP_400_BAD_REQUEST
            )

        serializer = StreamPlatformSerializer(platform,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status = HTTP_200_OK
            )
        else:
            return Response(
                serializer.errors,
                status = HTTP_400_BAD_REQUEST
            )

    def delete(self,request,pk):
        try:
            platform = StreamPlatform.objects.get(pk = pk)
        except StreamPlatform.DoesNotExist:
            return Response(
                {"error : Platform not found"},
                status = HTTP_400_BAD_REQUEST
            )
        platform.delete()
        return Response(
            status=HTTP_204_NO_CONTENT
        )


### ApiView
class WatchListAV(APIView):
    def get(self,request):
        movies = WatchList.objects.all()
        serializer = WatchListSerializer(movies, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)

    def post(self, request):
        serializer = WatchListSerializer(data=request.data)
        # si es valido que se guarde y retornamos
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class WatchListDetailAV(APIView):
    def get(self,request,pk):
        try:
            movie = WatchList.objects.get(pk = pk)
        except WatchList.DoesNotExist:
            return Response(
                {'error': 'WatchList not found'},
                status=status.HTTP_404_NOT_FOUND
        )
        serializer = WatchListSerializer(movie)
        return Response(
            serializer.data,
            status = status.HTTP_200_OK)

    def put(self, request,pk):
# necesitamos pasarle que registro modifica
        movie = WatchList.objects.get(pk = pk)
        serializer = WatchListSerializer(movie ,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status = status.HTTP_400_BAD_REQUEST
                )

    def delete(self,request,pk):
        movie = WatchList.objects.get(pk=pk)
        movie.delete()
        # se borra y mandamos que ya no hay contenido
        return Response(status= status.HTTP_204_NO_CONTENT)