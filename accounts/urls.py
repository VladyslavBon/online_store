from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (
    RegisterApiView,
    GetCurrentUserView,
    ChangePasswordView,
    UpdateProfileView,
    LogoutView,
)

app_name = "accounts"

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # path('register/', RegisterApiView.as_view(), name = 'api_register'),
    path("profile/", GetCurrentUserView.as_view(), name="profile"),
    path("change_password/", ChangePasswordView.as_view(), name="change_password"),
    path("update_profile/", UpdateProfileView.as_view(), name="auth_update_profile"),
    path("logout/", LogoutView.as_view(), name="auth_logout"),
]
