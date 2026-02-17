from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenBlacklistView
from accounts.views.company_view import CompanyView
from accounts.views.login_view import loginView
from accounts.views.register_view import RegisterView
from accounts.views.profile_view import ProfileView
from accounts.views.user_view import UserView

urlpatterns = [
    # Auth endpoints
    path('login/', loginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
    
    # User endpoints
    path('users/', UserView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserView.as_view(), name='user-detail'),
    
    # Profile endpoints
    path('profiles/', ProfileView.as_view(), name='profile-list'),
    path('profiles/<int:pk>/', ProfileView.as_view(), name='profile-detail'),
    
    # Company endpoints
    path('companies/', CompanyView.as_view(), name='company-list'),
    path('companies/<int:pk>/', CompanyView.as_view(), name='company-detail'),
]
