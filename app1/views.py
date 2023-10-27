from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginForm

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate

from django.contrib.auth.decorators import login_required

from django.contrib import messages
def home(request):

    return render(request, 'app1/index.html')

def register(request):

    form = CreateUserForm()

    if request.method == "POST":

        form = CreateUserForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(request, "Tạo tài khoản thành công!")

            return redirect("login")

    context = {'form':form}

    return render(request, 'app1/register.html', context=context)




def login(request):

    form = LoginForm()

    if request.method == "POST":

        form = LoginForm(request, data=request.POST)

        if form.is_valid():

            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:

                auth.login(request, user)

                return redirect("dashboard")

    context = {'form':form}

    return render(request, 'app1/login.html', context=context)

def user_logout(request):

    auth.logout(request)

    messages.success(request, "Đã đăng xuất!")

    return redirect("login")

@login_required(login_url='login')
def dashboard(request):

    return render(request, 'app1/dashboard.html')