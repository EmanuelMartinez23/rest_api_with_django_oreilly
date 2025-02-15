
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import StreamPlatformDetailAV, ReviewList, ReviewDetail, ReviewCreate, StreamPlatformVS, UserReview
from ..api.views import WatchListAV, WatchListDetailAV, StreamListAV

# creamos un router
# router = DefaultRouter()
# # registramos una ruta (la que va combinar dos metodos listar y detail)
# router.register('stream', StreamPlatformVS, basename='streamplatform')

urlpatterns = [
    # agregamos las urls de la app watchlist_app
    path('list/', WatchListAV.as_view(), name = 'watch-list'),
    path('<int:pk>/', WatchListDetailAV.as_view(), name = "watch-list-details"),
    path('stream/', StreamListAV.as_view(), name = "stream-list"),
    path('stream/<int:pk>', StreamPlatformDetailAV.as_view(), name = "stream-detail"),

    # url para crear una review para una pelicula
    path('<int:pk>/review-create/', ReviewCreate.as_view(), name = "review-create"),
    # url para las rviews de un sola pelicula
    path('<int:pk>/reviews/', ReviewList.as_view(), name = "review-list"),
    # una sola review de una sola movie
    path('review/<int:pk>/', ReviewDetail.as_view(), name = 'review-detail'),

    # path('review/<int:pk>', ReviewDetail.as_view(), name = 'review-detail'),
    # path('review', ReviewList.as_view(), name = 'review-list'),

    # viewsets and routers
    # incluimos el router
    # path('', include(router.urls))

    # for filter urls
    # path('review/<str:username>', UserReview.as_view(), name = 'user-review-detail'),
    path('review/', UserReview.as_view(), name = 'user-review-detail'),


]
