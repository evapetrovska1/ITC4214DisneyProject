from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_view, name='cart'), # Path for the cart
    path('add/<int:product_id>/', views.add_to_cart, name='add'), # Path for adding product
    path('remove/<int:product_id>/', views.remove_from_cart, name='remove'), # Path for removing product
    path('clear/', views.clear_cart, name='clear'), # Path for clearing the entire cart
    path('checkout/', views.checkout_view, name='checkout'), # Path for checkout
    path('shipping/', views.shipping_view, name='shipping'), # Path for shipping
    path('select_address/', views.select_address, name='select_address'),
    path('use_new_address/', views.use_new_address, name='use_new_address'), # Path for new address
    path('complete-order/', views.complete_order, name='complete_order'),
    path('order-success/', views.order_success, name='order_success'),
    

]