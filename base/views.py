from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Mark, User, Denomination, Author, Comment
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import MyUserCreationForm, MarkForm, UserForm
from .seeder import seeder_func
from django.contrib import messages


# Create your views here.


def home(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ""
    # seeder_func()
    # marks = Mark.objects.all()
    marks = Mark.objects.filter(Q(name__icontains=q) | Q(description__icontains=q) | Q(denomination__name__icontains=q))
    marks = list(dict.fromkeys(marks))
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
    return render(request,'base/delete.html', {'obj': mark})

def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password').lower()

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "Username doesn't exist!")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username or Password is incorrect!")

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

def add_mark(request):
    authors = Author.objects.all()
    denominations = Denomination.objects.all()
    form = MarkForm()

    if request.method == "POST":
        mark_author = request.POST.get('author')
        mark_denomination = request.POST.get('denomination')

        author, created = Author.objects.get_or_create(name=mark_author)
        denomination, created = Denomination.objects.get_or_create(name=mark_denomination)

        form = MarkForm(request.POST)

        new_mark = Mark(image=request.FILES['image'], name=form.data['name'], author=author,
                        description=form.data['description'], file=request.FILES['file'], creator=request.user)

        if not (Mark.objects.filter(file=new_mark.file) or Mark.objects.filter(name=new_mark.name)):
            new_mark.save()
            new_mark.denomination.add(denomination)
            return redirect('home')

    context = {'form': form, 'authors': authors, 'denominations': denominations}
    return render(request, 'base/add_mark.html', context)

@login_required(login_url='login')
def view(request, id):
    mark = Mark.objects.get(id=id)
    mark_comments = mark.comment_set.all().order_by('-created')
    if request.method =='POST':
        comment = Comment.objects.create(
            user=request.user,
            mark=mark,
            body=request.POST.get('body')
        )
    return render(request, 'base/view.html', {'mark': mark, 'comments': mark_comments})

def delete_mark(request, id):
    mark = Mark.objects.get(id=id)
    if request.method == 'POST':
        mark.image.delete() # ამ ორი ხაზის საშუალებით მარკის წაშლის დროს იშლება ფაილი და ფოტო ბაზიდანაც
        mark.file.delete()
        mark.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': mark})

@login_required(login_url='login')
def update_user(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', user.id)
    return render(request, 'base/update_user.html', {'form': form})


def delete_comment(request, id):
    comment = Comment.objects.get(id=id)
    mark = comment.mark
    if request.method == 'POST':
        comment.delete()
        return redirect('view', mark.id)
    return render(request, 'base/delete.html', {'obj': comment})


def more_page(request):

    return render(request, 'base/more.html')