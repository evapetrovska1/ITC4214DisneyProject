from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from products.models import Product
from .models import WishlistItem

# ------------------ VIEW FOR ADDING ITEMS TO WISHLIST  ------------------
@login_required # Require log in for this feature
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id) # Get the current product

    # Create the wishlist item (if it already doesn't exist - possible bcs of unique feature in models.py)
    WishlistItem.objects.get_or_create(
        user=request.user, 
        product=product
    )

    # Inform the user
    messages.success(request, f"Added {product.name} to your wishlist!")

    # Redirect to product list
    return redirect('products:product_list')


# ------------------ VIEW FOR DELETING ITEMS FROM WISHLIST  ------------------
@login_required # Require log in for this feature
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id) # Get the current product
  
    # Delete the wishlist entry if it exists
    WishlistItem.objects.filter( # First filter and then delete
        user=request.user,
        product=product
    ).delete()

    # Inform the user
    messages.success(request, f"Removed {product.name} from your wishlist!")

    # Redirect back to the previous page (HTTP_REFERER)
    # If there is no referer, fallback to product list
    return redirect(
        request.META.get('HTTP_REFERER', 'products:product_list')
    )