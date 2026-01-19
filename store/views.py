from rest_framework import generics
from .models import Product, Cart, CartItem
from .serializers import ProductSerializer, CartSerializer
from rest_framework.permissions import IsAuthenticated

class CartDetailView(generics.RetrieveUpdateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer    

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

def get_queryset(self):
        
        return Cart.objects.filter(user=self.request.user)