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
    wishlist_item, created = WishlistItem.objects.get_or_create(
        user=request.user,
        product=product
    )

    # If it's an AJAX request, return JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':

        return JsonResponse({
                'success': True,
                'message': f'Added {product.name} to wishlist!',
                'action': 'added',
                'product_id': product_id
        })
    

    # Regular request (HTTP)
    if created:
        messages.success(request, f'Added {product.name} to wishlist!')
    else:
        messages.info(request, f'{product.name} is already in your wishlist')

    # Redirect the user
    return redirect('products:product_list')


# ------------------ VIEW FOR DELETING ITEMS FROM WISHLIST  ------------------
@login_required # Require log in for this feature
@require_POST
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id) # Get the current product
  
    # Delete the wishlist entry if it exists
    wishlist_item = WishlistItem.objects.get(
        user=request.user,
        product=product
    )
    wishlist_item.delete()

    # If it is an AJAX request, return JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': f'Removed {product.name} from wishlist',
                'action': 'removed',
                'product_id': product_id
            })
    
    # Regular request
    messages.success(request, f'Removed {product.name} from wishlist')
    return redirect('products:product_list')


# ------------------ VIEW FOR SEEING ALL WISHLIST ITEMS  ------------------
@login_required
def wishlist_view(request):

    # Get all wishlist items from the current user
    wishlist_items = WishlistItem.objects.filter(user=request.user).select_related('product')

    # Get the total price
    # Calculate total price
    total_price = sum(item.product.price for item in wishlist_items)
    
    # Render the items and the counts
    context = {
        'wishlist_items': wishlist_items,
        'wishlist_count': wishlist_items.count(),
        'total_price': total_price,
    }

    return render(request, 'wishlist/wishlist.html', context)
