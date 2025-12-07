from django import forms
from accounts.models import Address

# Create a form for filling in the address
class ShippingForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['full_name', 'street_address', 'apartment', 'city', 'state', 'zip_code', 'country', 'phone']
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Full Name'}),
            'street_address': forms.TextInput(attrs={'placeholder': 'Street Address'}),
            'apartment': forms.TextInput(attrs={'placeholder': 'Apartment (optional)'}),
            'city': forms.TextInput(attrs={'placeholder': 'City'}),
            'state': forms.TextInput(attrs={'placeholder': 'State/Province'}),
            'zip_code': forms.TextInput(attrs={'placeholder': 'ZIP Code'}),
            'country': forms.TextInput(attrs={'placeholder': 'Country'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Phone Number (optional)'}),
        }