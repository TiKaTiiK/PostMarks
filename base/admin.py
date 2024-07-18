from django.contrib import admin
from .models import Mark, Author, User, Denomination

# Register your models here.
admin.site.register(Mark)
admin.site.register(Author)
admin.site.register(User)
admin.site.register(Denomination)
