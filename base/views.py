from django.shortcuts import render
from django.http import HttpResponse
from .models import Mark, User

# Create your views here.


def home(request):
    marks = Mark.objects.all()
    context = {"marks": marks}
    return render(request, 'base/home.html', context)


def about(request):
    return render(request, 'base/about.html')


def profile(request, st):
    user = User.objects.get(id=int(st))
    marks = user.marks.all()
    context = {'marks': marks, "user": user}
    return render(request,'base/profile.html', context)
