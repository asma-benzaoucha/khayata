from django.urls import path
from .views import TopSellingFashionModelsView
from .views import FashionModelListView,FashionModelFemmeListView,FashionModelHommeListView,FashionModelEnfantListView
from . import views
urlpatterns = [
    path('top-selling-models/', TopSellingFashionModelsView.as_view(), name='top-selling-models'),
      path('models/all', FashionModelListView.as_view(), name='model-list'),
      path('models/femmes/', FashionModelFemmeListView.as_view(), name='model-femme-list'),
      path('models/hommes/', FashionModelHommeListView.as_view(), name='model-homme-list'),
      path('models/enfants/', FashionModelEnfantListView.as_view(), name='model-enfant-list'),
      path('allorders/', views.get_my_orders, name='client-orders'),
      path('signup/', views.client_signup, name='client_signup'),
      path('delivery-price/', views.delivery_price_api, name='delivery-price'),




      
]