from watchlist_app.models import Movie
from watchlist_app.api.serializers import MovieSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

# view para regresar la lista de peliculas
@api_view(['GET', 'POST'])
def movie_list(request):
    # diferencia que metodo es
    if request.method == 'GET':
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    if request.method == 'POST':
        # se crea el archivo
        serializer = MovieSerializer(data = request.data)
        # si es valido que se guarde y retornamos
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data)
        else: 
            return Response(serializer.errors)



# view para ver el detalle de una pelicula
@api_view(['GET', 'PUT', 'DELETE'])
def movie_details(request, pk):
    if request.method == 'GET':
        try:
            movie = Movie.objects.get(pk = pk)
        except Movie.DoesNotExist:
            return Response(
                {'error': 'Movie not found'},
                status=status.HTTP_404_NOT_FOUND
        )
        serializer = MovieSerializer(movie)
        return Response(
            serializer.data,
            status = status.HTTP_200_OK)
    # modificar registro
    if request.method == 'PUT':
        # necesitamos pasarle que registro modifica
        movie = Movie.objects.get(pk = pk)
        serializer = MovieSerializer(movie ,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status = status.HTTP_400_BAD_REQUEST
                )

# borramos
    if request.method == 'DELETE':
        movie = Movie.objects.get(pk = pk)
        movie.delete()
        # se borra y mandamos que ya no hay contenido
        return Response(status= status.HTTP_204_NO_CONTENT)