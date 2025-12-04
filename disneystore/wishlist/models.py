from django.db import models
from django.conf import settings

# Create a model to store the wishlist items
class WishlistItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # Get the current user
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE) # Get the current item
    added_at = models.DateTimeField(auto_now_add=True) # Date and time item is added (for ordering)

    class Meta:
        # Prevent the same item from being added twice
        unique_together = ('user', 'product')

        # Newest items ordered first
        ordering = ['-added_at']

        # Add names for the items (Override the auto-generation from Django)
        verbose_name = "Wishlist Item"
        verbose_name_plural = "Wishlist Items"

    def __str__(self):
        return f"{self.user.username} ♥ {self.product.name}"

