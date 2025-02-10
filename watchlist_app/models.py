from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import CASCADE, Model, FloatField


# Create your models here.
class StreamPlatform(models.Model):
    name = models.CharField(max_length=30)
    about = models.CharField(max_length=150)
    website = models.URLField(max_length=100)

    def __str__(self):
        return self.name


class WatchList(models.Model):
    title = models.CharField(max_length=50)
    storyline = models.CharField( max_length=200)
    platform = models.ForeignKey(StreamPlatform, on_delete=CASCADE, related_name="watchlist")
    activate = models.BooleanField(default = True)
    # 3 el promedio del raiting
    avg_rating = models.FloatField(default = 0)
    # el id de la reseña
    number_rating = models.IntegerField(default=0)

    created = models.DateTimeField(auto_now_add=True)

    # el toString para nuestro modelo


    def __str__(self):
        return self.title

# creamos una request para las reviews de cada pelicula
class Review(models.Model):
    # añadir el usuario que crea la review
    review_user = models.ForeignKey(User, on_delete=models.CASCADE)
    # validamos que la review sea de 1 a 5
    rating = models.PositiveIntegerField(validators= [MinValueValidator(1), MaxValueValidator(5)])
    description = models.CharField(max_length=200, null = True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default = True)
    # un movie puede tener varias review
    watchlist = models.ForeignKey(WatchList, on_delete= CASCADE, related_name= 'reviews')

    def __str__(self):
        return f"{self.rating} | {self.watchlist.title}"