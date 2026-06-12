from django.urls import path
from .views import *

urlpatterns = [
    path('',home,name='customer_home'),
    path('restaurants/',restaurant_list,name='customer_restaurant_list'),
    path('foods/',food_list, name='food_list'),
    path('restaurant/<int:id>/',restaurant_detail,name='restaurant_detail'),
    path('add-to-cart/<int:id>/',add_to_cart,name='add_to_cart'),
    path('cart/',cart_list,name='cart_list'),
    path('increase-quantity/<int:id>/',increase_quantity,name='increase_quantity'),
    path('decrease-quantity/<int:id>/',decrease_quantity,name='decrease_quantity'),
    path('remove-item/<int:id>/',remove_item,name='remove_item'),
    path('place-order/',place_order,name='place_order'),
    path('orders/',order_history,name='order_history'),
    path('logout/', logout_view, name='logout'),
    path('delivery-details/',delivery_details,name='delivery_details'),
    path('order-success/',order_success,name='order_success'),
    path('payment/', payment, name='payment'),
    path('track-order/', track_order, name='track_order'),
    path('delivered/', delivered, name='delivered'),
    path('review/', review_page, name='review_page'),
    path('reviews/', review_list, name='review_list'),
]