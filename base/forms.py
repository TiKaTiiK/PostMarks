from django.contrib.auth.forms import UserCreationForm
from .models import User, Mark
from django.forms import ModelForm



class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class MarkForm(ModelForm):
    class Meta:
        model = Mark
        fields = '__all__'

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'username', 'email', 'bio', 'marks']