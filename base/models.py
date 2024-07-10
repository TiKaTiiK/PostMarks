from django.db import models

# Create your models here.


class Mark(models.Model):
    author = models.CharField(max_length=200)
    image = models.CharField(max_length=300)
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=300)
    content = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name} _ {self.author}"
