from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.models import User
from django.forms import DateInput
from django import forms
from .models import Room, Comment, Booking
from django.contrib.admin.widgets import AdminDateWidget
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

class DateInput(forms.DateInput):
    input_type = 'date'

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['Đánh_giá','Nhận_xét']

class BookingForm(forms.ModelForm):

    class Meta:
        widgets = {'check_in':DateInput(),'check_out':DateInput()
        }
        model = Booking
        fields = ['check_in', 'check_out']
