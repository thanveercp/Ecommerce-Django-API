from django.db import models
from django.conf import settings

class Category(models.Model):
    name=models.CharField(max_length=100)
    slug=models.SlugField(unique=True)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    category = models.ForeignKey(Category,related_name='products',on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    image_url = models.URLField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Cart(models.Model):
    # ഏത് യൂസറുടേതാണ് ഈ കാർട്ട് എന്ന് തിരിച്ചറിയാൻ
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    # ഒരു കാർട്ടിൽ ഒന്നിലധികം പ്രോഡക്റ്റുകൾ ഉണ്ടാകാം
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
def __str__(self):
        return f"{self.quantity} x {self.product.name}"