from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_products, name='products'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('add/', views.add_product, name='add_product'),
    path('edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('product_detail/rate/<int:product_id>/', views.rate_product, name='rate_product'),
    path('product_detail/edit/<int:product_id>/<int:review_id>/', views.edit_review, name='edit_review'),
    path('products/product_detail/delete/<int:product_id>/<int:review_id>/', views.delete_review, name='delete_review'),
]