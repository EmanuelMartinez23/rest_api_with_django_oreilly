
from django.urls import path
from ..api.views import MovieListAV , MovieDetailAV
urlpatterns = [
    # agregamos las urls de la app watchlist_app
    path('list/', MovieListAV.as_view(), name = 'movie-list'),
    path('<int:pk>', MovieDetailAV.as_view(), name = "movie-details")
]
