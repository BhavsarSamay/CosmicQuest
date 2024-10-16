from django.db import models
from datetime import timedelta
from django.utils import timezone

class CustomUser(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Store the hashed password
    phone = models.CharField(max_length=15, blank=True, null=True)  # Optional phone number

    def __str__(self):
        return self.username


def get_expiration_date():
    """Return the expiration date for the token (7 days from now)."""
    return timezone.now() + timedelta(days=7)

class Token(models.Model):
    key = models.CharField(max_length=40, primary_key=True)  # Primary key for the token
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set the creation date
    expires_at = models.DateTimeField(default=get_expiration_date)  # Token expires in 7 days

    def is_valid(self):
        """Check if the token is still valid based on the expiration date."""
        return self.expires_at > timezone.now() if self.expires_at else False

    class Meta:
        db_table = 'tokens'  # Explicitly set the table name if needed


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('book', 'Books'),
        ('clothes', 'Clothes'),
        ('home_decor', 'Home Decor'),
    ]
    
    name = models.CharField(max_length=150)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)  # URL for the product image
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'products' 

class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)  # Number of products in the cart

    class Meta:
        unique_together = ('user', 'product')  # Ensure a user cannot add the same product multiple times

    def __str__(self):
        return f"{self.user.username}'s cart: {self.product.name} (Quantity: {self.quantity})"
