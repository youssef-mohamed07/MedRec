from django.urls import path
from .views import (
    RegisterView, 
    ProfileView, 
    UpdateProfileView,
    ChangePasswordView,
    LogoutView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
    DeleteAccountView
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    # Registration & Authentication
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # Profile Management
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/update/', UpdateProfileView.as_view(), name='profile-update'),
    
    # Password Management
    path('password/change/', ChangePasswordView.as_view(), name='change-password'),
    path('password/reset/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('password/reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    
    # Account Deletion
    path('delete/', DeleteAccountView.as_view(), name='delete-account'),
]
