from django.db import models

# Create your models here.

class Movie(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField( max_length=200)
    activate = models.BooleanField(default = True)

    # el toString para nuestro modelo


    def __str__(self):
        return self.name
