from django.contrib import admin
from .models import Product, Category, Color, Rating

# Register the models created in the admin
admin.site.register(Category)
admin.site.register(Color)
admin.site.register(Rating)

# Function to automatically generate the URL of the product
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "color", "price", "stock", "created_at")
    prepopulated_fields = {"slug": ("name",)}  # auto-fill slug from name
