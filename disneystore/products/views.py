from django.shortcuts import render, get_object_or_404
from .models import Product, Category, Color, ProductRating
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import models


# ------------------ VIEW FOR LISTING ALL OF THE PRODUCTS ------------------ 
def product_list(request):
    # Get the filters applied from the user
    category_id  = request.GET.get("category")
    color_id = request.GET.get("color")
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")

    # Start with all of the products
    products = Product.objects.all()

    # Define the category/color names for rendering later
    selected_category_name = None
    selected_color_name = None

    # ------ CATEGORY FILTER ------
    # If the category filter is applied, filter the products according to it
    if category_id:
        products = products.filter(category_id=category_id)
    
    # ------ COLOR FILTER ------
    # The same here for color
    if color_id:
        products = products.filter(color_id=color_id)

    # ------ PRICE FILTERS (slider implemented) ------
    if min_price:
        products = products.filter(price__gte=min_price)
    
    if max_price:
        products = products.filter(price__lte=max_price)

    # Get the main categories (the parent ones) and the colors to be displayed
    main_categories = Category.objects.filter(parent__isnull=True)
    colors = Color.objects.all()

    # ------ GET THE NAMES OF THE CATEGORY AND COLOR (for display of current active filters) ------
    if category_id:
        try:
            cat = Category.objects.get(id=category_id) # Get the id
            selected_category_name = cat.name # Get the name
        except:
            pass # If error arises, pass
    
    if color_id:
        try:
            cat = Color.objects.get(id=color_id) # Get the id
            selected_color_name = cat.name # Get the name
        except:
            pass # If error arises, pass
    
    context = {
        'products': products,
        'main_categories': main_categories,
        'colors': colors,
        'selected_category': category_id, # Get id of category
        'selected_category_name': selected_category_name, # Get name of category
        'selected_color': color_id, # Get id of color
        'selected_color_name': selected_color_name, # Get name of color
        'min_price': min_price,
        'max_price': max_price,
    }

    return render(request, 'products/product_list.html', context)




# ------------------ VIEW FOR INDIVIDUAL PRODUCT PAGES ------------------
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    category = product.category

    # Product is in a subcategory
    if category.parent is not None:
        # Recommend products from the same subcategory
        related_products = Product.objects.filter(
            category=category
        ).exclude(id=product.id).order_by('?')[:3]

    else:
        # Product is in a main category
        # Retrieve subcategories of this main category
        subcategories = category.subcategories.all()

        if subcategories.exists():
            # Recommend products from all subcategories under this main category
            related_products = Product.objects.filter(
                category__in=subcategories
            ).exclude(id=product.id).order_by('?')[:3]
        else:
            # Main category with NO subcategories (e.g., Uncategorized)
            related_products = Product.objects.filter(
                category=category
            ).exclude(id=product.id).order_by('?')[:3]


    return render(request, 'products/product_detail.html', {
        'product': product,
        'related_products': related_products,
    })



# ------------------ VIEW FOR RATING A PRODUCT ------------------
@login_required
@require_POST
def rate_product(request):
    product_id = request.POST.get('product_id')
    stars = request.POST.get('stars')
    
    try:
        stars = int(stars)
        if not 1 <= stars <= 5:
            raise ValueError
    except:
        return JsonResponse({'success': False, 'error': 'Invalid rating'})
    
    product = get_object_or_404(Product, id=product_id)
    
    # Update or create rating using ProductRating model
    ProductRating.objects.update_or_create(
        product=product,
        user=request.user,
        defaults={'stars': stars}
    )
    
    # Calculate new average
    avg = product.ratings.aggregate(models.Avg('stars'))['stars__avg']
    avg = round(avg or 0, 1)
    count = product.ratings.count()
    
    return JsonResponse({
        'success': True,
        'average': avg,
        'count': count,
        'your_rating': stars
    })
