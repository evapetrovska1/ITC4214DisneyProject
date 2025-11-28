from django.urls import path
from . import views

# Define the app name
app_name = 'products'

# Paths for viewing the products
urlpatterns = [
    path('', views.product_list, name='product_list'),  # /products/
    path('<int:pk>/', views.product_detail, name='product_detail'),  # /products/1/
]