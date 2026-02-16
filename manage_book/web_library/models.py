from django.db import models

class Books(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    isbn = models.IntegerField()

    def __str__(self):
        return self.title

