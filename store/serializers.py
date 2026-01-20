from rest_framework import serializers
from django.db import transaction
from .models import Product, Category, Cart, CartItem, Order, OrderItem

# --- 1. PRODUCT SERIALIZER ---
class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock', 'image_url', 'category_name']


# --- 2. CART SERIALIZERS ---
class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at', 'items', 'total_price']

    def get_total_price(self, obj):
        # Calculate total price of all items in the cart
        return sum(item.product.price * item.quantity for item in obj.items.all())


# --- 3. ORDER SERIALIZERS ---
class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'unit_price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'placed_at', 'payment_status', 'items']


class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.IntegerField()

    def save(self, **kwargs):
        # Using atomic transaction to ensure data integrity
        with transaction.atomic():
            user_id = self.context['user_id']
            cart_id = self.validated_data['cart_id']

            # Create the parent order record
            order = Order.objects.create(user_id=user_id)

            # Retrieve items from the cart
            cart_items = CartItem.objects.select_related('product').filter(cart_id=cart_id)
            
            order_items = []
            for item in cart_items:
                product = item.product
                
                # Inventory check before creating order
                if product.stock < item.quantity:
                    raise serializers.ValidationError(f"Insufficient stock for {product.name}!")
                
                # Deduct stock from the product model
                product.stock -= item.quantity 
                product.save()

                # Prepare OrderItem objects
                order_items.append(OrderItem(
                    order=order,
                    product=product,
                    quantity=item.quantity,
                    unit_price=product.price
                ))

            # Bulk create order items for better performance
            OrderItem.objects.bulk_create(order_items)
            
            # Clear the cart after a successful order
            Cart.objects.filter(pk=cart_id).delete()

            return order