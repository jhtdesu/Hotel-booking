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
<<<<<<< HEAD
    path('room_list', views.roomlist, name='room_list')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
=======
    path('room_list', views.roomlist, name='room_list'),
    path('list', views.list, name= 'list'),
]
>>>>>>> f7acefd751871731c26098a1ac5c1b80fefda453
