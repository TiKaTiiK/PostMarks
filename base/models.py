from django.db import models
from django.contrib.auth.models import AbstractUser
class Author(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Denomination(models.Model):
    objects = None
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name

# Create your models here.
class Mark(models.Model):
    creator = models.ForeignKey('User', on_delete=models.SET("Unknown Creator"))
    author = models.ForeignKey(Author, on_delete=models.SET("Unknown Author"))
    image = models.ImageField(null=True, blank=True)
    name = models.CharField(max_length=200)
    denomination = models.ManyToManyField(Denomination, blank=True, related_name='marks')
    description = models.TextField(max_length=300)
    file = models.FileField(null=True)

    created = models.DateTimeField(auto_now_add=True)
    # updated = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ["created"]


    def __str__(self):
        return f"{self.name} _ {self.author}"

class User(AbstractUser):
    marks = models.ManyToManyField(Mark, blank=True, related_name='users')
    bio = models.TextField(null=True)
    avatar = models.ImageField(null=True, default='avatar.svg')

