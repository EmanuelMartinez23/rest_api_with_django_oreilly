
from django.urls import path

from .views import StreamPlatformDetailAV
from ..api.views import WatchListAV, WatchListDetailAV, StreamListAV
urlpatterns = [
    # agregamos las urls de la app watchlist_app
    path('list/', WatchListAV.as_view(), name = 'watch-list'),
    path('<int:pk>', WatchListDetailAV.as_view(), name = "watch-list-details"),
    path('stream/', StreamListAV.as_view(), name = "stream-list"),
    path('stream/<int:pk>', StreamPlatformDetailAV.as_view(), name = "stream-detail")
]
