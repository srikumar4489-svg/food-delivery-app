from django.urls import path
from .views import *

urlpatterns = [
    path('add-restaurant/',add_restaurant,name='add_restaurant'),
    path('restaurant-list/',restaurant_list,name='restaurant_list'),
    path('add-food/',add_food,name='add_food'),
    path('food-list/',food_list,name='food_list'),
    path('edit-food/<int:id>/',edit_food,name='edit_food'),
    path('delete-food/<int:id>/',delete_food,name='delete_food'),
]