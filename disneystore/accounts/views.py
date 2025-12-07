from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from wishlist.models import WishlistItem

# ------------------ VIEW FOR USER REGISTRATION ------------------
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST) # Create the form with user input
        if form.is_valid():
            user = form.save() # Save the new user to the databaseChat
            login(request, user) # Automatically log them in
            messages.success(request, 'Welcome to the Disney Family!')
            return redirect('products:product_list') # Redirect users directly to the products page
        else:
            messages.error(request, 'Please fix the errors :)')

    # If it isn't a post, it is a GET method (get the template with the form)
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})




# ------------------ VIEW FOR USER LOGIN ------------------
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST) # Create authentication form with submitted data
        if form.is_valid():
            # Extract the data from the form
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # Authenticate the user
            user = authenticate(username=username, password=password)

            # If authentication was successful
            if user is not None:
                login(request, user) # Log the user in
                messages.success(request, f'Welcome back, {username}')
                return redirect('products:product_list') # Redirect user to the products page
            
            # Authentication failed
            else:
                messages.error(request, 'Invalid username or password :(') 
        else:
            messages.error(request, 'Invalid username or password :(') # Form validation failed
    else: # GET request
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})




# ------------------ VIEW FOR USER LOGOUT ------------------
def logout_view(request):
    logout(request) # Log out the user

    messages.info(request, 'You succesfully logged out!')
    
    return redirect('products:product_list') # Again redirect user to products page




# ------------------ VIEW FOR USER PROFILE ------------------
@login_required # Users must log in before they access profile
def profile_view(request):

    # If the user wishes to change their data
    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name','').strip() # Strip the input of any trailing spaces
        request.user.last_name = request.POST.get('last_name','').strip() # Strip the input of any trailing spaces
        request.user.save() # Save the changes
    
        messages.success(request, "Profile updated successfully!")
        
        # Reload the page with the new data
        return redirect('accounts:profile')

    # Get the cart items from the current session
    cart = request.session.get('cart', {})
    cart_items = cart.values()
    cart_total = sum(float(item['price']) * item['quantity'] for item in cart_items)
    cart_count = sum(item['quantity'] for item in cart_items)

    # Get the wishlist items
    wishlist_items = WishlistItem.objects.filter(user=request.user).select_related('product')


    # Get all of the information
    context = {
        'join_date': request.user.date_joined.strftime("%B %Y"),
        'wishlist_items': wishlist_items,
        'cart_items': cart_items,
        'cart_total': cart_total,
        'cart_count': cart_count,
    }
    return render(request, 'accounts/profile.html', context)



# ------------------ VIEW FOR PASSWORD CHANGE ------------------
@login_required
def change_password_view(request):

    # Only work when the user submits the form (clicks the button)
    if request.method == 'POST':

        # Create the form
        form = PasswordChangeForm(request.user, request.POST)
        
        if form.is_valid():
            # Save the form
            user = form.save()
            
            # Important: update the session to prevent user logout
            update_session_auth_hash(request, user)

            # Display success message
            messages.success(request, 'Your password has been changed successfully!')
            return redirect('accounts:profile')
        else:
            # Display error message
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'accounts/change_password.html', {'form': form})
