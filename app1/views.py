from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginForm, Information, CommentForm, BookingForm

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate

from django.contrib.auth.decorators import login_required

from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from app1.models import Hotel, Room, Comment, Booking
from django.shortcuts import render, get_object_or_404
from .models import Room
from django.db.models import Q
from datetime import datetime
import datetime
import stripe
from django.db import IntegrityError
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
stripe.api_key = settings.STRIPE_SECRET_KEY
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

@login_required(login_url='login')
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
    comment = Comment.objects.filter(hotel__name=hotel.name)
    return render(request, 'app1/detail.html',{
        'hotel': hotel,
        'rooms' : rooms,
        'comment' : comment,
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

@login_required(login_url='login')
def comment(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    form = CommentForm()

    if request.method == "POST":

        form = CommentForm(request.POST)
        
        if form.is_valid():
            commentmodel = form.save(commit=False)
            commentmodel.created_by = request.user
            commentmodel.hotel_id = pk
            try: 
                commentmodel.save()
                messages.success(request, "Bình luận thành công!")
                return redirect("homepage")
            except IntegrityError as e: messages.error(request, "Bạn chỉ có thể đánh giá 1 lần đối với mỗi khách sạn")
            

            

    context = {'form': form}

    return render(request, 'app1/comment.html', context=context)

@login_required(login_url='login')
def bookinfo(request):
    bookings = Booking.objects.filter()

    return render(request, 'app1/bookinfo.html',{
        'bookings' : bookings,
    })

@login_required(login_url='login')
def pay(request):
    rooms = Room.objects.filter()

    return render(request, 'app1/pay.html',{
        'rooms' : rooms,
    })

@login_required(login_url='login')
def room(request, pk):
    bookings = Booking.objects.filter()
    rooms = get_object_or_404(Room, pk=pk)
    form = BookingForm(request.POST, instance=rooms)
    if request.method =="POST":
        
        check_in = request.POST.get('check_in')
        check_out = request.POST.get('check_out')
        ci = datetime.datetime.strptime(str(check_in),"%Y-%m-%d").date()
        case_1 = Booking.objects.filter(room = rooms, check_in__lte=check_in, check_out__gte=check_in).exists()
        case_2 = Booking.objects.filter(room = rooms, check_in__lte=check_out, check_out__gte=check_out).exists()
        case_3 = Booking.objects.filter(room = rooms, check_in__gte=check_in, check_out__lte=check_out).exists()
        if datetime.datetime.now().date()>=ci:
            messages.error(request, "Ngày không hợp lệ")
        elif(case_1 or case_2 or case_3):
            messages.error(request, "Lỗi")
        else:    
            rooms = Room.objects.filter()
            booking = Booking(
                check_in=check_in,
                check_out= check_out,  
                created_by=request.user,
                book_check="Còn hạn",
                room_id= pk,
            )
            rooms.is_booked = True
            booking.save()
            return redirect("homepage")
            messages.success(request, "Bạn đã đặt phòng thành công")
    return render(request, 'app1/room.html',{
        'rooms' : rooms,
        'form' : form,
        'bookings' : bookings,
    })

@login_required(login_url='login')
def cancel(request, pk):
    bookings = Booking.objects.get(pk = pk)
    bookings.delete()
    messages.success(request,"Hủy phòng thành công")
    return redirect("bookinfo")

@login_required(login_url='login')
def bookedroom(request,pk):
    bookings = Booking.objects.filter(pk = pk)
    rooms = Room.objects.filter(pk = pk)
    return render(request, 'app1/bookedroom.html',{
        'bookings' : bookings,
        'rooms' : rooms,
    })
def CreateSessionStripeView(request,pk):
    bookings = Booking.objects.get(pk = pk)
    
    pay_session = stripe.checkout.Session.create(
            payment_method_types = ["card"],
            line_items =[
                {
                    "price_data":{
                        "currency":"vnd",
                        "unit_amount":int(bookings.room.price),
                        "product_data":{
                            "name":bookings.room.hotel.name,
                            "description":bookings.room.name,
                            "images":[
                                f"{bookings.room.image}"
                            ],
                        },
                    },
                    "quantity":1,
                }
            ],
            metadata={"product_id":bookings.pk},
            mode = "payment",
            success_url = "http://127.0.0.1:8000/success",
            cancel_url = "http://127.0.0.1:8000/cancelpay"
    ) 
    return redirect(pay_session.url)    
def cancelpay(request):
    messages.error(request, "Thanh toán thất bại")
    return render(request,'app1/homepage.html')
def success(request):
    # booking = Booking.objects.filter(pk = pk,instance=booking)
    # booking.pay_status = True
    # booking.save()
    messages.success(request, "Thanh toán thành công")
    return render(request, 'app1/homepage.html')
@csrf_exempt
def stripe_webhook(request):
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None
    try: event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        product_id = session["metadata"]["product_id"]
        bookings = Booking.objects.get(id=int(product_id))
        bookings.pay_status = True
        bookings.save()
    return HttpResponse(status=200)