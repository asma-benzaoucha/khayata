from django.urls import path
from .views import TopSellingFashionModelsView
from .views import FashionModelListView,FashionModelFemmeListView,FashionModelHommeListView,FashionModelEnfantListView,SocialLinksList
from . import views
urlpatterns = [
    path('top-selling-models/', TopSellingFashionModelsView.as_view(), name='top-selling-models'),
      path('models/all', FashionModelListView.as_view(), name='model-list'),
      path('models/femmes/', FashionModelFemmeListView.as_view(), name='model-femme-list'),
      path('models/hommes/', FashionModelHommeListView.as_view(), name='model-homme-list'),
      path('models/enfants/', FashionModelEnfantListView.as_view(), name='model-enfant-list'),
      path('allorders/', views.get_client_orders, name='client-orders'),
      path('signup/', views.client_signup, name='client_signup'),
      path('delivery-price/', views.delivery_price_api, name='delivery-price'),
      path('validatecodepromo/<str:code>/<str:modelCode>/', views.validate_promo_code, name='validate_promo_code'),     
      path('achetermodel/', views.create_order, name='create_order'),
      path('changename/', views.change_client_name, name='change_client_name'),
      path('specialcommand/', views.create_special_command, name='special-command'),
      path('sociallinks/', SocialLinksList.as_view(), name='social-links'),







      
]