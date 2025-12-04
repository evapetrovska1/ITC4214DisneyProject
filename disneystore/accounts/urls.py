from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'), # Login
    path('register/', views.register_view, name='register'), # Registration
    path('logout/', views.logout_view, name='logout'), # Logout
    path('profile/', views.profile_view, name='profile'), # Profile
    path('change-password/', views.change_password_view, name='change_password'), # Profile
]