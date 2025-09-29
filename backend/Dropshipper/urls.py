
from django.urls import path
from . import views
from .views import (DropshipperSignupView)
urlpatterns = [
    path('signup/', DropshipperSignupView.as_view(), name='dropshipper-signup'), 
    path('checkStatusDropshipper/<str:email>', views.check_status_dropshipper, name='check_status_dropshipper'),
    path('top-demandingmodels/', views.get_top_selling_models, name='top-selling-models'),

]