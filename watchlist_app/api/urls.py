
from django.urls import path
from watchlist_app.api.views import movie_list, movie_details
urlpatterns = [
    # agregamos las urls de la app watchlist_app
    path('list/', movie_list, name = 'movie-list'),
    path('<int:pk>', movie_details, name = "movie-details")
]
