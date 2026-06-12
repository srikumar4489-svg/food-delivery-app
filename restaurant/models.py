from django.db import models

class Restaurant(models.Model):

    name = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=10)
    image = models.ImageField(upload_to='restaurant_images/',null=True,blank=True)

    def __str__(self):
        return self.name



class Food(models.Model):

    restaurant = models.ForeignKey(Restaurant,on_delete=models.CASCADE)


    name = models.CharField(max_length=100)

    description = models.TextField()

    price = models.IntegerField()

    image = models.ImageField(upload_to='food_images/')

    def __str__(self):
        return self.name