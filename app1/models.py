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
    created_by = models.ForeignKey(User, related_name='admin',on_delete=models.CASCADE,default=1)

    def __str__(self):
        return '%s-%s'%(self.name, self.created_by)
    
class Comment(models.Model):
    hotel = models.ForeignKey(Hotel, related_name="comments", on_delete=models.CASCADE)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='user_comments',on_delete=models.CASCADE)
    def __str__(self):
        return '%s-%s'%(self.hotel.name,self.created_by)

class Booking(models.Model):
    room = models.ForeignKey(Room, related_name="room_book", on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    created_by = models.ForeignKey(User, related_name="user_book",on_delete=models.CASCADE)
    def __str__(self):
        return 'book from %s to %s in room %s at hotel %s by %s'%(self.check_in,self.check_out,self.room.name,self.room.hotel.name,self.created_by)
    # def save(self):
    #     if(self.check_in <= self.check_out):
    #         return super().save()