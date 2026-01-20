from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import MyTokenObtainPairView, ProfileDetailView

urlpatterns = [
    # JWT Authentication Endpoints
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # User Profile Endpoint
    path('profile/', ProfileDetailView.as_view(), name='profile-detail'),
]