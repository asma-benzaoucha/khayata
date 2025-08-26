from django.urls import path
from .views import (CouturiereSignupView, CustomTokenObtainPairView,ResetPasswordView, verify_email, 
                    ResendVerificationEmailView ,ForgotPasswordView, VerifyOTPView,)
from django.http import HttpResponse
from . import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)
urlpatterns = [
    
    path('signup-couturiere/', CouturiereSignupView.as_view(), name='signup-couturiere'),
    path('resend-verification/', ResendVerificationEmailView.as_view(), name='resend-verification'),
    path('verify-email/<str:uid>/<str:token>/', verify_email, name='verify_email'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path("forgot-password/", ForgotPasswordView.as_view()),
    path("verify-otp/", VerifyOTPView.as_view()),
    path("reset-password/",ResetPasswordView.as_view()),
    path('changepassword/', views.change_password, name='change_password'),
    
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('nameclient/', views.get_client_name, name='get_client_name'),



]


