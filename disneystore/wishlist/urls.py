from django.urls import path
from . import views

app_name = 'wishlist'

urlpatterns = [
    path('add/<int:product_id>/', views.add_to_wishlist, name='add'), # Path for adding product
    path('remove/<int:product_id>/', views.remove_from_wishlist, name='remove'), # Path for removing product
]