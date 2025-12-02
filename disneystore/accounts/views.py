from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages


# ------------------ VIEW FOR USER REGISTRATION ------------------
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST) # Create the form with user input
        if form.is_valid():
            user = form.save() # Save the new user to the databaseChat
            login(request, user) # Automatically log them in
            messages.success(request, 'You have been registered, WELCOME!')
            return redirect('products:product_list') # Redirect users directly to the products page
        else:
            messages.error(request, 'Please fix the errors :)')

    # If it isn't a post, it is a GET method (get the template with the form)
    else:
        form = UserCreationForm()
    
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
def profile_view(request):
    return render(request, 'accounts/profile.html')


