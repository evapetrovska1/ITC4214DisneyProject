from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from products.models import Product
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .forms import ShippingForm
from accounts.models import Address, Order, OrderItem
from django.urls import reverse
import time
from django.contrib.auth import get_user_model
from products.models import Product
from django.db import transaction

# ------------------ VIEW FOR ADDING ITEMS TO CART  ------------------
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id) # Get the current product (like in the wishlist)
    cart = request.session.get('cart',{}) # Build the cart for the current user's session

    # Use session instead of making objects because cart items aren't permanent - the wishlist is

    # Convert to string (Django saves session variables in JSON which means numbers can't be stored properly)
    product_id_str = str(product_id)

    # If product is already in the cart, increase the quantity
    if product_id_str in cart:
        cart[product_id_str]['quantity'] += 1
    # Else, add the product to the cart
    else:
        # Create the product object inside of the cart
        cart[product_id_str] = {
            'id': product.id,
            'name': product.name,
            'price': str(product.price),
            'quantity': 1, # Initialize the quantity to 1
            'image_url': product.image.url if product.image else None,
            'description': product.description,
        }

    request.session['cart'] = cart

    # Check if it is an AJAX request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        cart_count = sum(item['quantity'] for item in cart.values())

        return JsonResponse({
                'success': True,
                'message': 'Item removed from cart',
                'cart_count': cart_count,
                'product_id': product_id
        })
    
    # For regular request, redirect the user
    messages.success(request, f"Added {product.name} to cart!") # Inform the user
    return redirect('cart:cart') # Bring the user back to the cart
        


# ------------------ VIEW FOR REMOVING ITEMS FROM CART  ------------------
def remove_from_cart(request, product_id):
    cart = request.session.get('cart',{}) # Get the cart from the user's current session
    
    # Get the product
    product_id_str = str(product_id)

    if product_id_str in cart:
        # If the quantity is greater than 1, decrease it
        if cart[product_id_str]['quantity'] > 1:
            cart[product_id_str]['quantity'] -= 1
        # Else, delete the item
        else:
            del cart[product_id_str]
        
        # Inform the user and save the cart
        request.session['cart'] = cart
    
    # Check if the request is AJAX
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            cart_count = sum(item['quantity'] for item in cart.values())
            
            return JsonResponse({
                'success': True,
                'message': 'Item removed from cart',
                'cart_count': cart_count,
                'product_id': product_id
            })
    
        
    # For regular request, redirect the user
    messages.success(request, "Item removed from cart") # Inform the user
    return redirect('cart:cart') # Bring the user back to the cart



# ------------------ VIEW FOR VIEWING ALL ITEMS  ------------------
# Doesn't need @require_POST cause it is a GET request, not POST
def cart_view(request):
    cart = request.session.get('cart',{}) # Get the current cart from the user's session

    # Get the total price (item price * quantity for each)
    total_price = sum(float(item['price']) * item['quantity'] for item in cart.values())

    # The context
    context = {
        'cart_items': cart.values(),
        'total_price': total_price,
        'item_count': sum(item['quantity'] for item in cart.values()) # Item count total
    }

    return render(request, 'cart/cart.html', context)



# ------------------ VIEW FOR CLEARING ALL ITEMS  ------------------
# We make a view for clearing all items instead of looping Ajax for simplicity
def clear_cart(request):
    request.session['cart']={}
    messages.success(request, "Cart cleared")
    return redirect('cart:cart')



# ------------------ VIEW FOR CHECKING OUT  ------------------
def checkout_view(request):
    cart = request.session.get('cart',{}) # Get the cart from user's session

    # If the cart is empty, redirect user back to cart
    if not cart:
        messages.error("Your cart is empty!")
        return redirect('cart:view')
    
    # Calculate the total price
    total_price = sum(float(item['price']) * item['quantity'] for item in cart.values())

    # The context
    context = {
        'cart_items': cart.values(),
        'total_price': total_price,
        'item_count': sum(item['quantity'] for item in cart.values()) # Item count total
    }

    return render(request, 'cart/checkout.html', context)


# ------------------ VIEW FOR SHIPPING  ------------------
def shipping_view(request):
    # Get the current cart
    cart = request.session.get('cart', {})

    # If cart doesn't exist - redirect the user
    if not cart:
        messages.error(request, "Your cart is empty!")
        return redirect('cart:cart')

    # Get user's saved addresses if logged in
    user_addresses = Address.objects.filter(user=request.user) if request.user.is_authenticated else []

    # If they submit their address
    if request.method == 'POST':
        form = ShippingForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            if request.user.is_authenticated:
                address.user = request.user
            address.save()
            # Save address ID to session for guest/logged-in
            request.session['shipping_address_id'] = address.id
            return redirect('cart:payment')  # Next step
    else:
        form = ShippingForm()

    total_price = sum(float(item['price']) * item['quantity'] for item in cart.values())

    context = {
        'shipping_form': form,
        'user_addresses': user_addresses,
        'cart_items': cart.values(),
        'total_price': total_price,
    }
    return render(request, 'cart/shipping.html', context)



# ------------------ VIEW FOR SELECTING ADDRESS ------------------
@require_POST
def select_address(request):
    # Get address_id from POST data, not URL
    address_id = request.POST.get('address_id')

    if not address_id:
        return JsonResponse({'success': False, 'message': 'No address selected'})
    if request.user.is_authenticated:
        try:
            address = Address.objects.get(id=address_id, user=request.user)
            # Store address ID in session
            request.session['shipping_address_id'] = address.id
            return JsonResponse({
                'success': True,
                'message': 'Address selected',
                'address_id': address.id
            })
        except Address.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Address not found'
            })
    return JsonResponse({
        'success': False,
        'message': 'Please log in to use saved addresses'
    })


# ------------------ VIEW FOR USING NEW ADDRESS ------------------
@require_POST
def use_new_address(request):

    # Get the form data
    form = ShippingForm(request.POST)
    if form.is_valid():
        address_data = form.cleaned_data
        
        # If the user is logged in, save the data and render it right away
        if request.user.is_authenticated:
            # Logged-in user: save to database
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            address_id = address.id
            
            # Render the new address in place
            return JsonResponse({
                'success': True,
                'message': 'Address saved to your account',
                'address': {
                    'id': address.id,
                    'full_name': address.full_name,
                    'street_address': address.street_address,
                    'city': address.city,
                    'state': address.state,
                    'zip_code': address.zip_code,
                    'country': address.country,
                    'phone': address.phone or ''
                },
                'saved_to_account': True
            })
        
        # Guest user, so store the address in session only
        else:
            # Get the data
            address_id = f"temp_{int(time.time())}"
            request.session['temp_address'] = address_data
            request.session['shipping_address_id'] = address_id
            request.session.modified = True
            
            # Return the data
            return JsonResponse({
                'success': True,
                'message': 'Address saved for checkout',
                'address': address_data,  # Send back the cleaned data
                'saved_to_account': False,
                'is_temp': True
            })
    
    # Form is invalid
    return JsonResponse({
        'success': False,
        'errors': form.errors
    })



# ------------------ VIEW FOR COMPLETING ORDER ------------------
def complete_order(request):
    if request.method != 'POST':
        return redirect('cart:shipping')

    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "Cart is empty!")
        return redirect('cart:shipping')

    from django.contrib.auth import get_user_model
    User = get_user_model()

    # Get user or guest
    user = request.user if request.user.is_authenticated else User.objects.get_or_create(
        username='guest',
        defaults={'first_name': 'Guest'}
    )[0]

    total_price = sum(float(item['price']) * item['quantity'] for item in cart.values())

    try:
        # Using transaction.atomic to ensure all operations complete togethe
        with transaction.atomic():
            # Create order
            order = Order.objects.create(
                user=user,
                total_price=total_price,
                status='Processing'
            )

            for product_id_str, item in cart.items():
                product = Product.objects.get(id=int(product_id_str))
                quantity = item['quantity']

                # Create order items
                OrderItem.objects.create(
                    order=order,
                    product_name=item['name'],
                    product_price=item['price'],
                    quantity=item['quantity']
                )

                # Decrease the stock
                product.stock -= quantity
                product.save()
        
            # Clear cart
            request.session['cart'] = {}
            request.session.modified = True

            request.session['last_order_id'] = order.id
            messages.success(request, f"Order #{order.id} placed successfully!")
            return redirect('cart:order_success')
    
    # Handle exception
    except Exception as e:
        messages.error(request, f"An error occurred while processing your order: {str(e)}")
        return redirect('cart:checkout')



# ------------------ VIEW FOR SUCCESS  ------------------
def order_success(request):
    order_id = request.session.get('last_order_id')
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        order = None
    
    context = {
        'order': order
    }
    return render(request, 'cart/order_success.html', context)