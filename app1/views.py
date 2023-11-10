from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginForm, Information, CommentForm

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate

from django.contrib.auth.decorators import login_required

from django.contrib import messages
from django.contrib.auth.models import User

from app1.models import Hotel, Room
from django.shortcuts import render, get_object_or_404
from .models import Room
from django.db.models import Q

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

                return redirect("homepage")

    context = {'form':form}

    return render(request, 'app1/login.html', context=context)
@login_required(login_url='login')
def user_logout(request):

    auth.logout(request)

    messages.success(request, "Đã đăng xuất!")

    return redirect("login")


def homepage(request):
    hotels = Hotel.objects.filter()
    return render(request, 'app1/homepage.html',{
        'hotels': hotels,
    })



@login_required(login_url='login')
def editinfo(request):
    form = Information()
    if request.method == "POST":

        form = Information(request.POST, instance=request.user)

        if form.is_valid():

            form.save()
            messages.success(request, "Cap nhat")
            return redirect("homepage")
    context = {'form':form}
    return render(request, 'app1/editinfo.html', context=context)
@login_required(login_url='login')
def info(request):
   
    return render(request, 'app1/info.html')
@login_required(login_url='login')
def roomlist(request):
    rooms = Room.objects.filter(is_booked=False)[0:6]
    hotels = Hotel.objects.all()

    return render(request, 'app1/room_list.html',{
        'hotels':hotels,
        'rooms':rooms,
    })
@login_required(login_url='login')
def detail(request, pk):
    # room = get_object_or_404(Room, pk=pk)
    hotel = get_object_or_404(Hotel, pk=pk)
    rooms = Room.objects.filter(hotel__name=hotel.name)

    return render(request, 'app1/detail.html',{
        'hotel': hotel,
        'rooms' : rooms,
    })

def room(request, pk):
    rooms = get_object_or_404(Room, pk=pk)

    return render(request, 'app1/room.html',{
        'rooms' : rooms,
    })

@login_required(login_url='login')
def list(request):
    return render(request, 'app1/list.html')
@login_required(login_url='login')
def search(request):
    query = request.GET.get('query', '')
    hotels = Hotel.objects.filter()
    if query:
        hotels = hotels.filter(Q(name__icontains=query) |Q(description__icontains=query)|Q(location__icontains=query)|Q(adress__icontains=query))

    return render(request, 'app1/search.html', {
        'hotels': hotels,
        'query': query,

    })
def comment(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    form = CommentForm()

    if request.method == "POST":

        form = CommentForm(request.POST)

        if form.is_valid():
            commentmodel = form.save(commit=False)
            commentmodel.created_by = request.user
            commentmodel.hotel_id = pk
            commentmodel.save()
            messages.success(request, "Bình luận thành cong(gay)!")

            return redirect("homepage")

    context = {'form': form}

    return render(request, 'app1/comment.html', context=context)