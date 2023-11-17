from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
import datetime
from django.core.validators import MaxValueValidator,MinValueValidator
# Create your models here.
Book_choices = ( 
    ("Còn hạn", "Còn hạn"), 
    ("Hết hạn", "Hết hạn"), 
) 
Rate_choices = (
    ("1","1"),
    ("1.5","1.5"),
    ("2","2"),
    ("2.5","2.5"),
    ("3","3"),
    ("3.5","3.5"),
    ("4","4"),
    ("4.5","4.5"),
    ("5","5"),
)
class Hotel(models.Model):
    price_max = models.IntegerField(default= 1000000)
    price_min = models.IntegerField(default= 1)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='hotel_images',blank=True,null=True)
    totalroom = models.IntegerField(default=0)
    description = models.TextField(blank=True, null=True)
    adress = models.TextField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    rating_average = models.FloatField(default=0)
    review_count = models.IntegerField(default=0)
    def canculator_price(self):
        hotel_room = self.hotel_room.all()
        self.price_max = hotel_room.aggregate(models.Max('price')).get('price__max')
        self.price_min = hotel_room.aggregate(models.Min('price')).get('price__min')
        self.totalroom = hotel_room.count()
        self.save(update_fields=['price_max','totalroom','price_min'])
    def canculator_rate(self):
        comments=self.comments.all()
        self.rating_average = comments.aggregate(models.Avg('Đánh_giá')).get('Đánh_giá__avg')
        self.review_count = comments.count()
        self.save(update_fields=['rating_average','review_count'])

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name
    
class Room(models.Model):
    hotel = models.ForeignKey(Hotel, related_name='hotel_room',on_delete=models.CASCADE)
    beds = models.IntegerField(default=1)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.IntegerField(default=100)
    image = models.ImageField(upload_to='room_images',blank=True,null=True)
    is_booked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='admin',on_delete=models.CASCADE,default=1)
    def save(self, *args, **kwargs):
        super(Room, self).save(*args, **kwargs)
        self.hotel.canculator_price()

    def __str__(self):
        return '%s-%s'%(self.name, self.hotel)
    
class Comment(models.Model):
    hotel = models.ForeignKey(Hotel, related_name="comments", on_delete=models.CASCADE)
    Nhận_xét = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='user_comments',on_delete=models.CASCADE)
    Đánh_giá = models.FloatField(validators=[MinValueValidator(1),MaxValueValidator(5)],default=5)
    class Meta:
        unique_together = ['created_by', 'hotel']
    def __str__(self):
        return '%s-%s'%(self.hotel.name,self.created_by)
    def save(self, *args, **kwargs):
        super(Comment, self).save(*args, **kwargs)
        self.hotel.canculator_rate()

class Booking(models.Model):
    room = models.ForeignKey(Room, related_name="rooms", on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    created_by = models.ForeignKey(User, related_name="user",on_delete=models.CASCADE)
    book_date = models.DateTimeField(auto_now_add=True)
    book_check = models.CharField(max_length= 20,choices=Book_choices)
    pay_status = models.BooleanField(default=False)
    def __str__(self):
        if (datetime.datetime.now().date()>=self.check_in):
            self.book_check = "Hết hạn"
            self.save()
        else: self.book_check = "Còn hạn" 
        return 'book from %s to %s in room %s at hotel %s by %s at %s'%(self.check_in,self.check_out,self.room.name,self.room.hotel.name,self.created_by, self.book_date)
    # def save(self):
    #     if(self.check_in <= self.check_out):
    #         return super().save()