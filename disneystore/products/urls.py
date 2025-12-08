from django.urls import path
from . import views

# Define the app name
app_name = 'products'

# Paths for viewing the products
urlpatterns = [
    path('', views.product_list, name='product_list'),  # /products/
    path('rate/', views.rate_product, name='rate_product'), # Rating each product
    path('product/<slug:slug>/', views.product_detail, name='product_detail'), # Viewing each individual product
]