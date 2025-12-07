from django.shortcuts import render

from django.contrib.auth.decorators import login_required, user_passes_test
from products.models import Product

def is_employee(user):
    # Django's built in methods to check user status
    return user.is_staff or user.is_superuser 
    # Will return true if user is employee/superuser

@login_required
@user_passes_test(is_employee)
def home(request):
    return render(request, 'employee_dash/home.html')
                