from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# 1. ആദ്യം റൂട്ടർ ഡിക്ലയർ ചെയ്യണം
router = DefaultRouter()

# 2. എന്നിട്ട് വേണം രജിസ്റ്റർ ചെയ്യാൻ
router.register('orders', views.OrderViewSet, basename='orders')

# 3. URL patterns സെറ്റ് ചെയ്യുക
urlpatterns = [
    path('', include(router.urls)), # റൂട്ടർ യുആർഎല്ലുകൾ ഇവിടെ വരും
    path('products/', views.ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('cart/<int:pk>/', views.CartDetailView.as_view(), name='cart-detail'),
]