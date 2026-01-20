from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Profile
from .serializers import ProfileSerializer

# --- 1. CUSTOM JWT LOGIN VIEW ---
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Customizing JWT token to include additional user information like username.
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        return token

class MyTokenObtainPairView(TokenObtainPairView):
    """
    View to handle user login and provide JWT access/refresh tokens.
    """
    serializer_class = MyTokenObtainPairSerializer


# --- 2. USER PROFILE VIEW ---
class ProfileDetailView(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update the profile of the currently authenticated user.
    """
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Automatically get the profile for the logged-in user
        # or create one if it doesn't exist.
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile