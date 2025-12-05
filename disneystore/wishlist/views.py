from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from products.models import Product
from .models import WishlistItem
from django.http import JsonResponse
from django.views.decorators.http import require_POST

# ------------------ VIEW FOR ADDING ITEMS TO WISHLIST  ------------------
@login_required # Require log in for this feature
@require_POST
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id) # Get the current product

    # Check if item is already in wishlist
    if WishlistItem.objects.filter(user=request.user, product=product).exists():
        return JsonResponse({'status': 'already_exists'}, status=200) # Return already exists message

    # Otherwise, add item to wishlist
    WishlistItem.objects.create(user=request.user, product=product)

    # Return success
    return JsonResponse({'status': 'added'}, status=200)


# ------------------ VIEW FOR DELETING ITEMS FROM WISHLIST  ------------------
@login_required # Require log in for this feature
@require_POST
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id) # Get the current product
  
    # Delete the wishlist entry if it exists
    deleted,_ = WishlistItem.objects.filter( # First filter and then delete
        user=request.user,
        product=product
    ).delete()

    if deleted:
        return JsonResponse({'status': 'removed'}, status=200)
    else:
        return JsonResponse({'status': 'not_found'}, status=200)
    


# ------------------ VIEW FOR SEEING ALL WISHLIST ITEMS  ------------------
@login_required
def wishlist_view(request):

    # Get all wishlist items from the current user
    wishlist_items = WishlistItem.objects.filter(user=request.user).select_related('product')

    # Get the total price
    # Calculate total price
    total_price = sum(item.product.price for item in wishlist_items)
    
    # Render the items and the coutns
    context = {
        'wishlist_items': wishlist_items,
        'wishlist_count': wishlist_items.count(),
        'total_price': total_price,
    }

    return render(request, 'wishlist/wishlist.html', context)
