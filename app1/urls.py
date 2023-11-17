from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('', views.home, name=""),

    path('register', views.register, name="register"),

    path('login', views.login, name="login"),

    path('user-logout', views.user_logout, name="user-logout"),

    path('homepage', views.homepage, name="homepage"),
    path('editinfo', views.editinfo, name="editinfo"),
    path('info', views.info, name="info"),
    path('room_list', views.roomlist, name='room_list'),
    path('list', views.list, name= 'list'),
    path('search', views.search, name= 'search'),
    path('detail/<int:pk>/', views.detail, name= 'detail'),
    path('room/<int:pk>/', views.room, name='room'),
    path('comment/<int:pk>/', views.comment, name='comment'),
    path('cancel/<int:pk>/', views.cancel, name='cancel'),
    path('bookedroom/<int:pk>/', views.bookedroom, name='bookedroom'),
    path('bookinfo', views.bookinfo,name='bookinfo'),
    path('payment/<int:pk>/', views.CreateSessionStripeView,name='payment'),
    path("success/", views.success, name="success"),
    path("cancelpay/", views.cancelpay, name="cancelpay"),
    path("stripe_webhook/",views.stripe_webhook,name="stripe_webhook")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
