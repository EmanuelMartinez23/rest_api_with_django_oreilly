from time import struct_time
from warnings import filters

from django.contrib.messages import warning
from django.core.serializers import serialize
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_204_NO_CONTENT
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle
from rest_framework.views import APIView

from .pagination import WatchListPagination, WatchListLOPagination, WatchListCPagination
from .permissions import IsAdminOrReadOnly, IsReviewUserOrReadOnly
from .serializers import StreamPlatformSerializer, ReviewSerializer
from .throttling import ReviewListThrottle, ReviewCreateThrottle
from ..models import WatchList, StreamPlatform, Review
from ..api.serializers import WatchListSerializer
from rest_framework.response import Response
from rest_framework import status, generics, mixins
from rest_framework import viewsets

# viewset y routers crear una vies para trabajhaer con una sola URL con dos objetivos listar y detail
# literal hacer una view para dos urls, tratar dos peticiones con una view
# class StreamPlatformVS(viewsets.ViewSet):
#     def list(self, request):
#         queryset = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(queryset, many=True)
#         return Response(serializer.data)
#
#     def retrieve(self,request, pk=None):
#         queryset = StreamPlatform.objects.all()
#         stream_platform = get_object_or_404(queryset,pk=pk)
#         serializer = StreamPlatformSerializer(stream_platform)
#         return Response(serializer.data)
#
#     def create(self, request):
#         serializer = StreamPlatformSerializer(data =  request.data)
#         if  serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)

# ModewlviewSet, da todo crud completo
#  ReadOnlyModelViewSet de igual manera se puede para readonlymodelviewset, solo que este solo da listar y detail
class StreamPlatformVS(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer

class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewCreateThrottle]
    # Conseguimos todos los valores para el filtro para saber si el user ya hizo reseña a dicha movie
    def get_queryset(self):
        return Review.objects.all()

    # no queryset ya que creamos
    # sobreescribimos el metodo de create una review
    def perform_create(self, serializer):
        # conseguimos el pk de la url
        pk  = self.kwargs.get('pk')
        watchlist = WatchList.objects.get(pk = pk)
        # conseguimos el usuarios
        review_user = self.request.user
        # filtramos y verificamos si el user ya hizo reseña en dicha move

        review_queryset =Review.objects.filter(watchlist =watchlist, review_user =review_user )
        # mensaje de error
        if review_queryset.exists():
            raise ValidationError("You have already reviewed this movie!")

        if watchlist.number_rating == 0 : # no hay ninguna reseña por ende es el mismo valor de la review
            watchlist.avg_rating = serializer.validated_data['rating']
        else :
            # si no sumamos lo que tenemos en avg_rating más lo de la review actual eso entre dos
            watchlist.avg_rating = (watchlist.avg_rating + serializer.validated_data['rating'])/2
        # sumanos al contador/Id de rating para esa pelicula,contador
        watchlist.number_rating = watchlist.number_rating +1
        watchlist.save()
        # guardamos la review
        serializer.save(watchlist = watchlist, review_user=review_user)

# view basada en clases concretas listar y crear reviews
class ReviewList(generics.ListCreateAPIView):
    # queryset = Review.objects.all() // no porque necesitamos solo las reviews de una movie
    serializer_class = ReviewSerializer
    # pagination_class = WatchListPagination
    # pagination_class = WatchListLOPagination
    pagination_class = WatchListCPagination
    # agregamos permisos a personas solo auth
    # permission_classes = [IsAuthenticatedOrReadOnly]
    # permission_classes = [IsAuthenticated]
    # custom permission
    # permission_classes = [AdminOrReadOnly]
    throttle_classes = [ReviewListThrottle]
    #
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username', 'active']

    # Searching
    # filter_backends = [filters.SearchFilter]
    # search_fields = ['review_user__username', 'active']

    # Ordering
    # filter_backends = [filters.OrderingFilter]
    # ordering_fields = ['review_user__username', 'active']

    # necesitamos sobreescribir el queryset
    def get_queryset(self):
        # conseguimos el pk parametro
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)


# view basada en clases concreta para indivduales reviews
class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    # throttle_classes = [UserRateThrottle, AnonRateThrottle]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'review-detail'

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = [AdminOrReadOnly]
    permission_classes = [IsReviewUserOrReadOnly]


# view con mixins para individuales review
# class ReviewDetail(mixins.RetrieveModelMixin,
#                    generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
#
#
#
# # de prueba ya que con views de clases concretas es más rapido
# class ReviewList(mixins.ListModelMixin, # listas las reviews (get opptimizado)9
#                  mixins.CreateModelMixin, # post optimizado, crear Review
#                  generics.GenericAPIView # clase padre  una generica de APIView
#                  ):
#     # queryset es un parametro de la clase GenericAPIView
#     queryset = Review.objects.all()
#     # serializer_class tambien es de la clase padre, debemos incidar el serializador del model
#     serializer_class = ReviewSerializer
#
#     # este metodo hacer todo lo que nosotros haciamos en APIView  y lista todos las reviews
#     # es el mismo de la doc
#     def get(self, request, *args,**kwargs):
#         return self.list(request, *args, **kwargs)
#     # mismo de la doc
#     def post(self,request, *args,**kwargs):
#         return self.create(request, *args, *kwargs)


class StreamListAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
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
    permission_classes = [IsAdminOrReadOnly]
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
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = WatchListPagination
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
    permission_classes = [IsAdminOrReadOnly]
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


class UserReview(generics.ListAPIView):
    serializer_class = ReviewSerializer
    # URL
    # def get_queryset(self):
    #     username = self.kwargs['username']
    #     return Review.objects.filter(review_user_username = username)

    def get_queryset(self):
        username = self.request.query_params.get('username',None)
        return Review.objects.filter(review_user__username = username)
