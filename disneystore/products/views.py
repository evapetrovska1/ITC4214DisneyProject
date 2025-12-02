from django.shortcuts import render
from django.db.models import Min, Max
from .models import Product, Category, Color


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

    # RENDER WITH ALL CONTEXT
    return render(request, 'products/product_list.html', {
        'products': products,
        'main_categories': main_categories,
        'colors': colors,
        'selected_category': category_id, # Get id of category
        'selected_category_name': selected_category_name, # Get name of category
        'selected_color': color_id, # Get id of color
        'selected_color_name': selected_color_name, # Get name of color
        'min_price': min_price,
        'max_price': max_price,
    })