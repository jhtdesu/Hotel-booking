from django.urls import path

from . import views

urlpatterns = [

    path('', views.home, name=""),

    path('register', views.register, name="register"),

    path('login', views.login, name="login"),

    path('user-logout', views.user_logout, name="user-logout"),

    path('homepage', views.homepage, name="homepage"),
    path('editinfo', views.editinfo, name="editinfo"),
    path('info', views.info, name="info"),
    path('room_list', views.roomlist, name='room_list')
]