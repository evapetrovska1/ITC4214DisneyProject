from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Product, Category, Color


# View defined for listing all products
def product_list(request):
    products = Product.objects.all()

    # Apply the filters from the parameters using GET
    category = request.GET.get("category")
    color = request.GET.get("color")
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")

    if category:
        products = products.filter(category__id=category)
    if color:
        products = products.filter(color__id=color)
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    # Define the categories and the colors to be displayed
    categories = Category.objects.all()
    colors = Color.objects.all()

    # Render the products, categories, and colors
    return render(request, 'products/product_list.html', {
        'products': products,
        'categories': categories,   
        'colors': colors,
    })

# View for a single product
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})