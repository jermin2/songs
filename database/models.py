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

    def serialize(self):
        return ({
            "title":self.title,
            "author":self.author,
            "composer":self.composer,
            "meter":self.meter,
            "key":self.key,
            "year":self.year,
            "content":self.content,
            "id":self.id
        })

    # Return a short serialization of just id and title
    def mini_serialize(self):
        return ({
            "id":self.id,
            "title":self.title
        })

