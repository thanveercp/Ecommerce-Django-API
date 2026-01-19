from django.urls import path
from .views import ProductListView,ProductDetailView,CartDetailView

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('cart/<int:pk>/', CartDetailView.as_view(), name='cart-detail'),
]