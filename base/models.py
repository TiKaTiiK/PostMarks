from django.db import models
from django.contrib.auth.models import AbstractUser
class Author(models.Model):
    name = models.CharField(max_length=200)
    birth = models.DateField(null=True)
    death = models.DateField(null=True)

    def __str__(self):
        return self.name

# Create your models here.
class Mark(models.Model):
    author = models.ForeignKey(Author, on_delete=models.SET("Unknown Author"))
    image = models.CharField(max_length=300)
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=300)
    content = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name} _ {self.author}"

class User(AbstractUser):
    marks = models.ManyToManyField(Mark, blank=True, related_name='Mark')