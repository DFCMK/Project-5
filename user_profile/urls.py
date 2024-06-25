from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('order_history/<order_number>', views.order_history, name='order_history'),
    path('profile/wishlist/', views.wishlist, name='wishlist'),
    path('wishlist/add_to_wishlist/<int:id>', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove_from_wishlist/<int:id>/', views.remove_from_wishlist, name='remove_from_wishlist')
    ]