from django.urls import path
from .views import (CouturiereSignupView, CustomTokenObtainPairView,ResetPasswordView, verify_email, 
                    ResendVerificationEmailView ,ForgotPasswordView, VerifyOTPView)

urlpatterns = [
    
    path('signup-couturiere/', CouturiereSignupView.as_view(), name='signup-couturiere'),
    path('resend-verification/', ResendVerificationEmailView.as_view(), name='resend-verification'),
    path('verify-email/<str:uid>/<str:token>/', verify_email, name='verify_email'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path("forgot-password/", ForgotPasswordView.as_view()),
    path("verify-otp/", VerifyOTPView.as_view()),
    path("reset-password/",ResetPasswordView.as_view()),

]


