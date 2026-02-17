from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.serializers.register_serializer import RegisterSerializer

class RegisterView(APIView):
    """
    Register endpoint that creates a new user and returns JWT tokens.
    Public endpoint - no authentication required.
    """
    permission_classes = (AllowAny,)
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            
            return Response({
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                },
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "message": "User registered successfully"
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)