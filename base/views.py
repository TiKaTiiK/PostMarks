from django.shortcuts import render
from django.http import HttpResponse
from .models import Mark, User, Denomination
from django.db.models import Q

# Create your views here.


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ""
    # marks = Mark.objects.all()
    marks = Mark.objects.filter(Q(name__icontains=q) | Q(description__icontains=q) | Q(denomination__name__icontains=q))
    marks = list(set(marks))
    # print(marks[0].users.all())
    denominations = Denomination.objects.all()
    heading = "Catalogue"
    context = {"marks": marks, "heading": heading, "denominations": denominations}
    return render(request, 'base/home.html', context)


def about(request):
    return render(request, 'base/about.html')

def contact(request):
    return render(request, 'base/contact.html')

def profile(request, st):
    user = User.objects.get(id=int(st))
    q = request.GET.get('q') if request.GET.get('q') != None else ""
    # marks = Mark.objects.all()
    marks = user.marks.filter(Q(name__icontains=q) | Q(description__icontains=q) | Q(denomination__name__icontains=q))
    marks = list(set(marks))
    denominations = Denomination.objects.all()
    heading = "My Stamps"
    context = {'marks': marks, "user": user, "heading": heading, "denominations": denominations}
    return render(request, 'base/profile.html', context)
