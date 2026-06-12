from django.shortcuts import render,redirect
from django.contrib.auth import logout
from restaurant.models import *
from .models import *

def home(request):

    return render(request, 'home.html')

def restaurant_list(request):

    restaurants = Restaurant.objects.all()

    return render(request,'restaurant_list1.html',{'restaurants': restaurants})

def food_list(request):

    foods = Food.objects.all()

    return render(request, 'food_list1.html', {'foods': foods})

def restaurant_detail(request, id):

    restaurant = Restaurant.objects.get(id=id)

    foods = Food.objects.filter(
        restaurant=restaurant
    )

    return render(request,'restaurant_detail.html',{'restaurant': restaurant,'foods': foods})

def add_to_cart(request, id):

    food = Food.objects.get(id=id)

    Cart.objects.create(
        food=food
    )

    return redirect('cart_list')


def cart_list(request):

    carts = Cart.objects.all()

    subtotal = 0

    for cart in carts:
        subtotal +=cart.food.price * cart.quantity

    delivery_charges = 30

    tax = subtotal * 0.05

    total = subtotal + delivery_charges + tax

    return render(request,'cart_list.html',{'carts': carts,'subtotal':subtotal,'delivery_charge':delivery_charges,'tax':tax,'total':total})


def increase_quantity(request, id):

    cart = Cart.objects.get(id=id)

    cart.quantity += 1

    cart.save()

    return redirect('cart_list')


def decrease_quantity(request, id):

    cart = Cart.objects.get(id=id)

    if cart.quantity > 1:

        cart.quantity -= 1

        cart.save()

    return redirect('cart_list')


def remove_item(request, id):

    print("REMOVE CLICKED:", id)

    cart = Cart.objects.filter(id=id).first()

    print("FOUND CART:", cart)

    if cart:
        cart.delete()
        print("DELETED")

    return redirect('cart_list')


def place_order(request):

    carts = Cart.objects.all()

    for cart in carts:

        Order.objects.create(
            food=cart.food,
            quantity=cart.quantity
        )

    carts.delete()

    return redirect('order_success')


def order_history(request):

    orders = Order.objects.all()

    return render(request,'order_history.html',{'orders': orders})

def logout_view(request):
    logout(request)
    return redirect('login')

def delivery_details(request):

    if request.method == "POST":

        Delivery.objects.create(
            name=request.POST['name'],
            phone=request.POST['phone'],
            address=request.POST['address'],
            city=request.POST['city'],
            pincode=request.POST['pincode']
        )

        return redirect('payment')

    return render(request, 'delivery_details.html')

def order_success(request):

    return render(request, 'order_success.html')

def payment(request):

    carts = Cart.objects.all()

    subtotal = 0

    for cart in carts:
        subtotal += cart.food.price * cart.quantity

    delivery_charge = 30

    tax = subtotal * 0.05

    total = subtotal + delivery_charge + tax

    return render(request,'payment.html',{'subtotal': subtotal,'delivery_charge': delivery_charge,'tax': tax,'total': total})

def track_order(request):

    return render(request, 'tracking.html')

def delivered(request):

    return render(request, 'delivered.html')

def review_page(request):

    if request.method == "POST":

        rating = request.POST.get("rating")
        review = request.POST.get("review")

        Review.objects.create(
            rating=rating,
            review=review
        )

        return render(request,'thank_you.html',{'rating': rating,'review': review})

    return render(request, 'review.html')

def review_list(request):

    reviews = Review.objects.all().order_by('-created_at')

    return render(request,'review_list.html',{'reviews': reviews})