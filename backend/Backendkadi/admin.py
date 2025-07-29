from django.contrib import admin
from .models import Client, FashionModel, CustomOrder, PromoCode ,livraison 

admin.site.register(Client)
admin.site.register(FashionModel)
admin.site.register(CustomOrder)
admin.site.register(PromoCode)
admin.site.register(livraison.WilayaDelivery)
