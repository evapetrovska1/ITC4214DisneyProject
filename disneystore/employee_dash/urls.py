from django.urls import path
from . import views

# Define the app name
app_name = 'employee_dash'

# Paths for viewing the dashboard
urlpatterns = [
    path('', views.home, name='home'),  # /employees_dash/
]