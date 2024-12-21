from watchlist_app.models import Movie
from watchlist_app.api.serializers import MovieSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view

# view para regresar la lista de peliculas
@api_view(['GET', 'POST'])
def movie_list(request):
    movies = Movie.objects.all()
    serializer = MovieSerializer(movies, many = True)
    return Response(serializer.data)

# view para ver el detalle de una pelicula
@api_view()
def movie_details(request, pk):
    movie = Movie.objects.get(pk = pk)
    serializer = MovieSerializer(movie)
    return Response(serializer.data)