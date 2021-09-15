from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    pass


class Book(models.Model):
    title =     models.CharField(max_length=255)
    songs =     models.ManyToManyField('Song', through='Song_Book', related_name="books")

    def __str__(self):
        return f'{self.title}({self.songs.count()})'


class Song_Book(models.Model):
    song =  models.ForeignKey('Song', on_delete=models.CASCADE, related_name="books")
    book =  models.ForeignKey('Book', on_delete=models.CASCADE, related_name='songs')
    index = models.IntegerField(max_length=10, blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['song', 'book'])
        ]

    def __str__(self):
        return f"{self.song} : {self.book.title} : {self.index}"

class Song(models.Model):
    title =     models.CharField(max_length=255)
    author =    models.CharField(max_length=255, blank=True)
    composer =  models.CharField(max_length=255, blank=True)
    meter =     models.CharField(max_length=255, blank=True)
    key =       models.CharField(max_length=10, blank=True)
    year =      models.IntegerField(max_length=10, blank=True, null=True)
    content =   models.CharField(max_length=1024)

    def __str__(self):
        return self.title

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

