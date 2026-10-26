from django.urls import path

# from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views

app_name = "users"
urlpatterns = [
    # path("login/", obtain_auth_token, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout, name="logout"),
    # use this for login
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
