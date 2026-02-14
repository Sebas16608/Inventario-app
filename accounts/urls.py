from django.urls import path

from accounts.views.register_view import RegisterAPIView
from accounts.views.login_view import LoginAPIView

from accounts.views.user_view import UserAPIView
from accounts.views.company_view import CompanyAPIView
from accounts.views.profile_view import ProfileAPIView

urlpatterns = [

    # Auth
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("login/", LoginAPIView.as_view(), name="login"),

    # Users
    path("users/me/", UserAPIView.as_view(), name="user-me"),

    # Company
    path("companies/", CompanyAPIView.as_view(), name="company-list-create"),
    path("companies/<int:pk>/", CompanyAPIView.as_view(), name="company-detail"),

    # Profile
    path("profile/", ProfileAPIView.as_view(), name="profile-me"),

]
