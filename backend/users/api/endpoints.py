from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from users.api.views import UserView

urlpatterns = [
    path('me', UserView.as_view(), name='profile'),
    path('auth', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token-refresh')
]
