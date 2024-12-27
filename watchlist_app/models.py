from django.db import models
from django.db.models import CASCADE


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
    created = models.DateTimeField(auto_now_add=True)

    # el toString para nuestro modelo


    def __str__(self):
        return self.title
