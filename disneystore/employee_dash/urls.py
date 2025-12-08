from django.urls import path
from . import views

# Define the app name
app_name = 'employee_dash'

# Paths for viewing the dashboard
urlpatterns = [
    path('', views.home, name='home'),  # /employees_dash/
    path('orders/', views.orders_management, name='orders'), # For the orders
    path('products/', views.products_management, name="products"), # For the products
    path('categories/', views.categories_management, name="categories"), # For the categories
]