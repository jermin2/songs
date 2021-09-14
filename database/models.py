from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    pass

class Song(models.Model):
    title =     models.CharField(max_length=255)
    author =    models.CharField(max_length=255, blank=True)
    composer =  models.CharField(max_length=255, blank=True)
    meter =     models.CharField(max_length=255, blank=True)
    key =       models.CharField(max_length=10, blank=True)
    year =      models.CharField(max_length=10, blank=True)
    content =   models.CharField(max_length=1024)

