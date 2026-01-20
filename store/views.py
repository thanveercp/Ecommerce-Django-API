from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import Product, Cart, Order
from .serializers import (
    ProductSerializer, CartSerializer, 
    OrderSerializer, CreateOrderSerializer
)

# --- 1. PRODUCT VIEWS ---

class ProductListView(generics.ListAPIView):
    """
    List all products with support for filtering, searching, and ordering.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    # Enable filtering backends
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    
    # Search by name or description (?search=item)
    search_fields = ['name', 'description']
    
    # Filter by category ID (?category=1)
    filterset_fields = ['category']
    
    # Order by price (?ordering=price or ?ordering=-price)
    ordering_fields = ['price']


class ProductDetailView(generics.RetrieveAPIView):
    """
    Retrieve details of a single product.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# --- 2. CART VIEWS ---

class CartDetailView(generics.RetrieveUpdateAPIView):
    """
    View or update the current user's cart.
    """
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Ensure users can only access their own cart
        return Cart.objects.filter(user=self.request.user)


# --- 3. ORDER VIEWS ---

class OrderViewSet(viewsets.ModelViewSet):
    """
    Handle creation and retrieval of orders. 
    Only admins can update (PATCH) or delete orders.
    """
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_permissions(self):
        # Restrict administrative actions to staff members only
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get_queryset(self):
        # Return only the orders belonging to the logged-in user
        # prefetch_related is used to optimize database queries for order items
        return Order.objects.filter(user=self.request.user).prefetch_related('items__product')

    def get_serializer_class(self):
        # Use a specific serializer for creating orders via POST
        if self.request.method == 'POST':
            return CreateOrderSerializer
        return OrderSerializer

    def get_serializer_context(self):
        # Pass the user ID to the serializer context for processing
        return {'user_id': self.request.user.id}