from django.shortcuts import render,redirect
from .models import *

def add_restaurant(request):

    if request.method == "POST":

        Restaurant.objects.create(
            name=request.POST['name'],
            address=request.POST['address'],
            phone=request.POST['phone'],
            image =request.FILES.get('image')
        )

    return render(request,'add_restaurant.html')

def restaurant_list(request):

    restaurants = Restaurant.objects.all()

    return render(
        request,
        'restaurant_list.html',
        {'restaurants': restaurants}
    )
from .models import Restaurant, Food, Category

def add_food(request):

    if request.method == "POST":

        restaurant = Restaurant.objects.get(
            id=request.POST.get("restaurant")
        )

        category = Category.objects.get(
            id=request.POST.get("category")
        )

        Food.objects.create(
            restaurant=restaurant,
            category=category,
            name=request.POST.get("name"),
            description=request.POST.get("description"),
            price=request.POST.get("price"),
            image=request.FILES.get("image")
        )

        return redirect('food_list')

    restaurants = Restaurant.objects.all()
    categories = Category.objects.all()

    return render(
        request,
        'add_food.html',
        {
            'restaurants': restaurants,
            'categories': categories
        }
    )

def food_list(request):

    foods = Food.objects.all()

    return render(request,'food_list.html',{'foods': foods})

def edit_food(request, id):

    food = Food.objects.get(id=id)

    if request.method == "POST":

        food.name = request.POST.get("name")
        food.description = request.POST.get("description")
        food.price = request.POST.get("price")

        if request.FILES.get("image"):
            food.image = request.FILES.get("image")

        food.save()

        return redirect('food_list')

    return render(request,'edit_food.html',{'food': food})

def delete_food(request, id):

    food = Food.objects.get(id=id)

    food.delete()

    return redirect('food_list')