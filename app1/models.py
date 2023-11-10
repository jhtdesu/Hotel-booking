from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here.
class Hotel(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='hotel_images',blank=True,null=True)
    totalroom = models.IntegerField(default=1)
    description = models.TextField(blank=True, null=True)
    adress = models.TextField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    rating = models.IntegerField(default=1)
    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name
    
class Room(models.Model):
    hotel = models.ForeignKey(Hotel, related_name='hotel',on_delete=models.CASCADE)
    beds = models.IntegerField(default=1)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField()
    image = models.ImageField(upload_to='room_images',blank=True,null=True)
    is_booked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    book_in = models.DateField(default=datetime.date.today)
    book_out = models.DateField(default=datetime.date.today)

    def __str__(self):
        return self.name