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
            try:
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
            except Exception as e:
                return Response({
                    "error": f"Error al crear el usuario: {str(e)}"
                }, status=status.HTTP_400_BAD_REQUEST)
        
        # Formatear errores para que sean más legibles
        error_messages = []
        for field, errors in serializer.errors.items():
            if isinstance(errors, list):
                error_messages.extend([f"{field}: {error}" for error in errors])
            else:
                error_messages.append(f"{field}: {errors}")
        
        return Response({
            "error": " | ".join(error_messages) if error_messages else "Error de validación"
        }, status=status.HTTP_400_BAD_REQUEST)