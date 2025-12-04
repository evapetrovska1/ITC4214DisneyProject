from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator

# Create the blueprint for the categorical filters
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True) # Category must be unique (it is the key)

    # Each category can reference its parent too (i.e. for the subcategories of the main ones)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE, # If the parent category is deleted, the subcategories are deleted as well
        related_name="subcategories",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name

# Create another one for the color (so the filters can be stackable)
class Color(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

# Create the fields for each product: name, description, price, number of stock, date posted, image and clean URLs
class Product(models.Model):
    # Individual fields for each product
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)       # linking the products with their names instead of IDs


    # Field for the category (type of product)
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_DEFAULT, # Set item as uncategorized if category is deleted
        related_name="products",
        default=1 # Set the default field to be uncategorized
    )

    # Field for the color
    color = models.ForeignKey(
        Color,
        on_delete=models.SET_DEFAULT, # Set item as uncategorized if category is deleted
        related_name="products",
        default=1 # Uncategorized
    )

    # Override the save method (instead of manually typing each product's name)
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            # Define what happens if duplicates arise
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}" # Include the number next to the name
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
 
class Rating(models.Model):
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        related_name="ratings" # Reverse relationship, so you can access rating.product and product.ratings.all() later on
    )
    # user = models.ForeignKey(User, on_delete=models.CASCADE) --------------------------- ADD USERS LATER ---------------------------
    stars = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(5)] # Set validators for the rating
    )
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # class Meta: --------------------------- AGAIN FOR THE USER ---------
    #     unique_together = ("product", "user")  # one rating per user per product

    def __str__(self):
        return f"{self.product.name} - {self.stars} stars"

