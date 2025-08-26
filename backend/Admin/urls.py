from django.urls import path
from .views import create_or_update_social_links

urlpatterns = [
    path('updatesociallinks/', create_or_update_social_links, name='social-links-create-update'),
]