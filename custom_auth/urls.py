from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('register/', UserRegistration.as_view(), name='register'),
    path('user_verification/', UserVerification.as_view(), name='user_verification'),
    path('login/', UserLogin.as_view(), name='login'),
    path('detail/<int:pk>/', UserDetail.as_view(), name='user_detail'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', UserLogout.as_view(), name='logout'),
    path('me/', UserDetail.as_view(), name='whoami'),
    path('resend_code/', EmailVerificationResend.as_view(), name='resend'),
    path('pong/', Ping.as_view(), name='ping'),
]