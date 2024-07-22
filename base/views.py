from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Mark, User, Denomination
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import MyUserCreationForm

# Create your views here.


def home(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ""
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
    q = request.GET.get('q') if request.GET.get('q') is not None else ""
    # marks = Mark.objects.all()
    marks = user.marks.filter(Q(name__icontains=q) | Q(description__icontains=q) | Q(denomination__name__icontains=q))
    marks = list(set(marks))
    denominations = Denomination.objects.all()
    heading = "My Stamps"
    context = {'marks': marks, "user": user, "heading": heading, "denominations": denominations}
    return render(request, 'base/profile.html', context)

@login_required(login_url='login')
def adding(request, id):
    mark = Mark.objects.get(id=id)
    user = request.user
    user.marks.add(mark)
    return redirect('profile', user.id)

@login_required(login_url='login')
def delete(request, id):
    mark = Mark.objects.get(id=id)
    if request.method == "POST":
        request.user.marks.remove(mark)
        return redirect('profile', request.user.id)
    return render(request,'base/delete.html', {'mark': mark})

def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password').lower()

        try:
            user = User.objects.get(username=username)
        except:
            pass #error message

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            pass #error mess

    return render(request, 'base/login.html')

def logout_user(request):
    logout(request)
    return redirect('home')

def register_page(request):
    form = MyUserCreationForm

    if request.method == "POST":
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/register.html', context)
