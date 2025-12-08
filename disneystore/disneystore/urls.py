"""
URL configuration for disneystore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls), # ADMIN urls
    path('', include('products.urls')), # Linking the products urls
    path('accounts/', include('accounts.urls')), # Linking the accounts urls
    path('wishlist/', include('wishlist.urls')), # Linking the wishlist urls
    path('employee_dash/', include('employee_dash.urls')), # Linking the employee dashboard urls
    path('cart/', include('cart.urls')), # Linking the cart urls
    path('pages/', include('pages.urls')),  # Static/general pages
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)