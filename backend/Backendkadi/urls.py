from django.urls import path
from .views import (
    CouturiereSignupView, 
    CustomTokenObtainPairView,
    ResetPasswordView,
    verify_email, 
    ResendVerificationEmailView ,
    ForgotPasswordView, 
    VerifyOTPView,
    CouturiereModelsView,
    DemandesFassouCouturiereModelsView,
    OffresFassouCouturiereModelsView,ModifyFassouOfferView,
    DemandesPersonaliseView,AffiliateOrdersView,
    CouturiereProfileView,
    AffiliatePromoCodeListView,
    AffiliateProfileView,
    AddModelView)
from django.conf import settings
from django.conf.urls.static import static

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
    path('changepasswordWithVerification/couturiere', views.change_password_with_verification, name='change_password'),

    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('nameclient/', views.get_client_name, name='get_client_name'),
    path('checkIfEmailExist/<str:email>', views.check_if_email_exists, name='check_if_email_exists'),
    path('nameclient/', views.get_client_name, name='get_client_name'),
    
    path("profile/couturiere/", CouturiereProfileView.as_view(), name="profile"),
    path("addmodel/", AddModelView.as_view(), name="addmodel"),
    path('mesmodels/', CouturiereModelsView.as_view(), name='mes-models'),
    path('MesDemandesFassou/', DemandesFassouCouturiereModelsView.as_view(), name='mes-models'),
    path('offresFassou/', OffresFassouCouturiereModelsView.as_view(), name='mes-models'),
    path('mesDemandesPersonalise/', DemandesPersonaliseView.as_view(), name='mes-models'),
    path("ModifyFassouOffer/<int:pk>/", ModifyFassouOfferView.as_view(), name="modify-fassou-offer"),
    
    path("affiliate/promocodes/", AffiliatePromoCodeListView.as_view(), name="affiliate-promocodes"),
    path("profile/affiliate/",AffiliateProfileView.as_view(), name="profile"),
    path("affiliate/orders/", AffiliateOrdersView.as_view(), name="affiliate-orders"),
    path('changepasswordWithVerification/affiliate', views.change_password_with_verification, name='change_password'),
    



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


