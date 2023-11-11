from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.models import User

from django import forms
from .models import Room, Comment

from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput

# - Register/Create a user

class CreateUserForm(UserCreationForm):

    class Meta:

        model = User
        fields = ['username', 'password1', 'password2']


# - Login a user

class LoginForm(AuthenticationForm):

    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())

class ChangePass(AuthenticationForm):
    password = forms.CharField(widget=PasswordInput())

class Information(UserChangeForm):
    User.email = forms.EmailField()
    User.first_name = forms.CharField()
    User.last_name = forms.CharField()
    class Meta:
        model = User
        fields = ( 'email', 'first_name', 'last_name')

class BookingForm(forms.ModelForm):

    class Meta:

        model = Room
        fields = ['book_in', 'book_out']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body',]
