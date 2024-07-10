from django.shortcuts import render
from django.http import HttpResponse
from .models import Mark

# Create your views here.


def home(request):
    marks = Mark.objects.all()
    context = {"marks": marks}
    return render(request, 'base/home.html', context)


def about(request):
    return render(request, 'base/about.html')


def profile(request):
    return render(request, 'base/profile.html')

