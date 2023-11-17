from django.contrib import admin
from .models import Room,Hotel,Comment,Booking
# Register your models here.

admin.site.register(Room)
admin.site.register(Hotel)
admin.site.register(Comment)
admin.site.register(Booking)