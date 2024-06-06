from django.db import models 
from member.models import User


DIVISION_CHOICES = [
        ('Dhaka', 'Dhaka'),
        ('Chittagong', 'Chittagong'),
        ('Rajshahi', 'Rajshahi'),
        ('Khulna', 'Khulna'),
        ('Barisal', 'Barisal'),
        ('Sylhet', 'Sylhet'),
        ('Rangpur', 'Rangpur'),
        ('Mymensingh', 'Mymensingh'),
    ]

class Apartment(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.TextField()
    bed = models.IntegerField()
    bath = models.IntegerField()
    division = models.CharField(choices=DIVISION_CHOICES, max_length=10)
    size = models.IntegerField()
    description = models.TextField()
    last_update = models.DateTimeField(auto_now=True)
    owner_id = models.IntegerField()

    def __str__(self):
        return f'{self.address} {self.division}'
    
class ApartmentImage(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name='images')
    image_url = models.URLField(max_length=200,default="")

    def __str__(self):
        return f'{self.apartment.address} {self.id}'


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    bookingDateTime = models.DateTimeField()
    createdAt = models.DateTimeField(auto_now_add=True)


class FavoriteApartment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)
    

    
    

    
