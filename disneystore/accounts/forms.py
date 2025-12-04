from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# CREATE CUSTOM USER FORM (because the prebuilt Django one only has username and password)
class CustomUserCreationForm(UserCreationForm):
    
    # Allow user to type in their first name
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget = forms.TextInput(attrs={'placeholder':'Mickey'})
    )

    # Allow user to type in their last name
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget = forms.TextInput(attrs={'placeholder':'Mouse'})
    )

    # Render all of the information in the User
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "password1", "password2")

    # Save the information
    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user