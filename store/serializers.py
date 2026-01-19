from rest_framework import serializers
from .models import Product, Category, Cart, CartItem

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock', 'image_url', 'category_name']

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity']

# ഈ ക്ലാസ് ആണ് നിങ്ങളുടെ ഫയലിൽ ഇല്ലാത്തത്. ഇത് കൃത്യമായി ചേർക്കുക.
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at', 'items', 'total_price']

    def get_total_price(self, obj):
        # കാർട്ടിലെ ഓരോ ഐറ്റത്തിന്റെയും വില കൂട്ടി ആകെ തുക കണക്കാക്കുന്നു
        return sum(item.product.price * item.quantity for item in obj.items.all())