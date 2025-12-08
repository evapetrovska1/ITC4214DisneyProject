from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count, Sum, Q
from django.utils import timezone
from datetime import timedelta
from products.models import Product, Category
from accounts.models import Order, OrderItem
from products.forms import ProductForm, CategoryForm

def is_employee(user):
    # Django's built in methods to check user status
    return user.is_staff or user.is_superuser 
    # Will return true if user is employee/superuser



# -------------------------- VIEW FOR HOME DASHBOARD --------------------------------------
@login_required
@user_passes_test(is_employee) # If the user passes the test, they can access the home page
def home(request):

    print("DEBUG: Dashboard view called")
    print(f"DEBUG: User: {request.user}, Is Staff: {request.user.is_staff}")

    # Get current time for date calculations
    now = timezone.now()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    week_start = today_start - timedelta(days=today_start.weekday())
    month_start = today_start.replace(day=1)

    # ORDER STATS
    total_orders = Order.objects.count()
    today_orders = Order.objects.filter(created_at__gte=today_start).count()
    week_orders = Order.objects.filter(created_at__gte=week_start).count()
    month_orders = Order.objects.filter(created_at__gte=month_start).count()

    # TOTAL REVENUE STATS
    total_revenue = Order.objects.aggregate(total=Sum('total_price'))['total'] or 0
    
    today_revenue = Order.objects.filter(
        created_at__gte=today_start
        ).aggregate(total=Sum('total_price'))['total'] or 0
    
    month_revenue = Order.objects.filter(
        created_at__gte=month_start
        ).aggregate(total=Sum('total_price'))['total'] or 0

    # Get total products count
    total_products = Product.objects.count();

    # Get total categories count (real data)
    total_categories = Category.objects.count()

    # ORDER STATUS
    processing_orders = Order.objects.filter(status='Processing').count()
    shipped_orders = Order.objects.filter(status='Shipped').count()
    delivered_orders = Order.objects.filter(status='Delivered').count()

    # TOTAL PRODUCTS
    total_products = Product.objects.count()

    # RETURN THE CONTEXT
    context = {
    # Order counts
    'total_orders': total_orders,
    'today_orders': today_orders,
    'week_orders': week_orders,
    'month_orders': month_orders,
    
    # Revenue
    'total_revenue': total_revenue,
    'today_revenue': today_revenue,
    'month_revenue': month_revenue,
    
    # Products
    'total_products': total_products,

    # Categories
    'total_categories': total_categories,
    # Order status
    'processing_orders': processing_orders,
    'shipped_orders': shipped_orders,
    'delivered_orders': delivered_orders,
    
    }
    return render(request, 'employee_dash/home.html', context)




# -------------------------- VIEW FOR ORDERS --------------------------------------
@login_required
@user_passes_test(is_employee) # If the user passes the test, they can access this page
def orders_management(request):
    # Get all orders sorted by date (newest first)
    all_orders = Order.objects.all().order_by('-created_at')

    # Filter all orders
    pending_orders = Order.objects.filter(status='Processing').order_by('-created_at')
    completed_orders = Order.objects.filter(status='Delivered').order_by('-created_at')
    
    context = {
        'all_orders': all_orders,
        'pending_orders': pending_orders,
        'completed_orders': completed_orders,
    }
    
    return render(request, 'employee_dash/orders.html', context)




# -------------------------- VIEW FOR ADDING/SEEING ALL PRODUCTS --------------------------------------
@login_required
@user_passes_test(is_employee) # If the user passes the test, they can access this page
def products_management(request):

    # Order products by id:
    products = Product.objects.all().order_by('-id')

    # The form
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Product added successfully!")
            return redirect('employee_dash:products')
    else:
        form = ProductForm()

    context = {
        'products': products,
        'form': form,
    }
    return render(request, 'employee_dash/products.html', context)
                
                

# -------------------------- VIEW FOR ADDING/SEEING ALL CATEGORIES --------------------------------------
@login_required
@user_passes_test(is_employee) # If the user passes the test, they can access this page
def categories_management(request):
    
    # Get all of the categories
    categories = Category.objects.filter(parent=None).prefetch_related('subcategories')

    # The form
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category added successfully!")
            return redirect('employee_dash:categories')
    else:
        form = CategoryForm()

    context = {
        'categories': categories,
        'form': form,
    }
    return render(request, 'employee_dash/categories.html', context)