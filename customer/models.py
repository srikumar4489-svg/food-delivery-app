from django.db import models
from restaurant.models import Food

class Cart(models.Model):

    food = models.ForeignKey(Food,on_delete=models.CASCADE)

    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.food.name
    

class Order(models.Model):

    food = models.ForeignKey(Food,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    ordered_at = models.DateTimeField(auto_now_add=True)

class Delivery(models.Model):

    name = models.CharField(max_length=100)

    phone = models.CharField(max_length=15)

    address = models.TextField()

    city = models.CharField(max_length=100)

    pincode = models.CharField(max_length=10)

    def __str__(self):
        return self.name
    
class Review(models.Model):

    rating = models.IntegerField()

    review = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.rating} Stars"