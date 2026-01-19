from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from.serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)