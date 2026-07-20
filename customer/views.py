from django.shortcuts import render,redirect
from django.contrib.auth import logout
from restaurant.models import *
from .models import *
from django.db.models import Q,Case, When, IntegerField
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
import random


def home(request):
    categories = Category.objects.all()
    return render(request, 'home.html',{'categories': categories})

def restaurant_list(request):

    restaurants = Restaurant.objects.all()

    return render(request,'restaurant_list1.html',{'restaurants': restaurants})

def food_list(request):

    foods = Food.objects.annotate(
        category_order=Case(
            When(category__name='Briyani', then=0),
            When(category__name='Chicken Gravy', then=1),
            When(category__name='Chicken Starters', then=2),
            When(category__name='Fried Rice', then=3),
            When(category__name='Noodles', then=4),
            When(category__name='Shawarma', then=5),
            When(category__name='KFC Chicken', then=6),
            When(category__name = 'Pizza', then=7),
            When(category__name='Fresh Juice',then=8),
            When(category__name='Milkshakes',then=9),
            default=99,
            output_field=IntegerField()
        )
    ).order_by('category_order', '-id')

    query = request.GET.get('q')

    if query and query.strip():

        foods = foods.filter(
            Q(name__icontains=query) |
            Q(category__name__icontains=query)
        )
    return render(request, 'food_list1.html', {'foods': foods})

def category_foods(request, id):

    category = Category.objects.get(id=id)

    foods = Food.objects.filter(category = category)

    return render(
        request,
        'category_foods.html',
        {
            'category': category,
            'foods': foods
        }
    )

def category_list(request):

    categories = Category.objects.all()

    return render(
        request,
        'category_list.html',
        {
            'categories': categories
        }
    )

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


# def place_order(request):

#     carts = Cart.objects.all()

#     for cart in carts:

#         Order.objects.create(
#             food=cart.food,
#             quantity=cart.quantity
#         )

#     carts.delete()

#     return redirect('order_success')




def place_order(request):

    delivery = Delivery.objects.last()

    customer_name = delivery.name
    phone = delivery.phone

    address = f"""
{delivery.address}
{delivery.city} - {delivery.pincode}
"""

    order_id = random.randint(100000, 999999)

    order_time = timezone.localtime().strftime(
        "%d-%m-%Y %I:%M %p"
    )

    carts = Cart.objects.all()

    order_details = ""
    total_amount = 0

    for cart in carts:

        Order.objects.create(
            food=cart.food,
            quantity=cart.quantity
        )

        item_total = cart.food.price * cart.quantity
        total_amount += item_total

        order_details += (
            f"{cart.food.name} x {cart.quantity} = ₹{item_total}\n"
        )

    send_mail(
        subject=f'New Order #{order_id}',
        message=f'''
Order ID: #{order_id}

Customer Name: {customer_name}

Phone Number: {phone}

Delivery Address:
{address}

Order Time:
{order_time}

--------------------------------

Ordered Items:

{order_details}

--------------------------------

Total Bill Amount: ₹{total_amount}

--------------------------------
''',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=['srikumar1122610@gmail.com'],
        fail_silently=False,
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

        user_name = request.user.first_name or request.user.email

        send_mail(
            subject = "🍔 Customer Review",
            message = f"""
            Customer : {user_name}
            ⭐ Rating : {rating}/5
            💬 Review : {review} """,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=["srikumar1122610@gmail.com"], 
            fail_silently=False,
        )

        return render(request,'thank_you.html',{'rating': rating,'review': review})

    return render(request, 'review.html')

def review_list(request):

    reviews = Review.objects.all().order_by('-created_at')

    return render(request,'review_list.html',{'reviews': reviews})