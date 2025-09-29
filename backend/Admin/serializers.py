
        




from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework import serializers

from Backendkadi.models.commandes import  CustomOrder 
from Backendkadi.models.user import  User ,Client
from Backendkadi.models.commandes import Order
from Backendkadi.models.modeles import  FashionModel
from Backendkadi.models.commandes import CustomOrder,Order
from Backendkadi.models.livraison import WilayaDelivery
from Backendkadi.models.promo import PromoCode
from Backendkadi.models.stock import StockVariantForCommands,StockVariantForFashionModels
from Backendkadi.models.socialAccountsLinkgroups import SocialAccountsLinkGroup


from Backendkadi.models.modeles import  FashionModel
from Backendkadi.models.modeles import ModelImage
from Backendkadi.models.commandes import CustomOrder,CustomOrderImage,Order
from Backendkadi.models.livraison import  WilayaDelivery
from Backendkadi.models.user  import User,Client,Dropshipper



User = get_user_model()

class WilayaDeliveryUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WilayaDelivery
        fields = ['wilaya_name', 'delivery_price']
        extra_kwargs = {
            'wilaya_name': {'validators': []}  # Désactive les validateurs d'unicité
        }

class BulkWilayaDeliverySerializer(serializers.Serializer):
    wilayas = WilayaDeliveryUpdateSerializer(many=True)
    
    def create(self, validated_data):
        wilayas_data = validated_data['wilayas']
        results = {
            'updated': [],
            'created': [],
            'errors': []
        }
        
        for wilaya_data in wilayas_data:
            try:
                wilaya_name = wilaya_data['wilaya_name']
                delivery_price = wilaya_data['delivery_price']
                
                # Utiliser update_or_create pour mettre à jour ou créer
                wilaya, created = WilayaDelivery.objects.update_or_create(
                    wilaya_name=wilaya_name,
                    defaults={'delivery_price': delivery_price}
                )
                
                if created:
                    results['created'].append({
                        'wilaya': wilaya_name,
                        'price': str(delivery_price)
                    })
                else:
                    results['updated'].append({
                        'wilaya': wilaya_name,
                        'price': str(delivery_price)
                    })
                    
            except Exception as e:
                results['errors'].append({
                    'wilaya': wilaya_data.get('wilaya_name', 'Unknown'),
                    'error': str(e)
                })
        
        return results
    
    
    


class WilayaDeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = WilayaDelivery
        fields = ['id', 'wilaya_name', 'delivery_price']
        read_only_fields = ['id', 'wilaya_name', 'delivery_price']
        
        
        
class StockVariantForFashionModelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockVariantForFashionModels
        fields = ['color', 'size', 'quantity']


class StockVariantForCommandsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockVariantForCommands
        fields = ['color', 'size', 'quantity']
        
        

class StockVariantSerializerforCustomCommands(serializers.ModelSerializer):
    class Meta:
        model = StockVariantForCommands
        fields = ['size', 'quantity']
        
        
        
        

class ModelImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelImage
        fields = ['image']

class FashionModelSerializer(serializers.ModelSerializer):
    variants = StockVariantForFashionModelsSerializer(many=True, read_only=True)
    images = ModelImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = FashionModel
        fields = [
            'id', 'name', 'code', 'type', 'description',
            'price_per_piece_for_client', 'price_per_piece_for_dropshipper',
            'min_pieces_for_dropshipper', 'state', 'owner', 'promo_code',
            'variants', 'images', 'created_at', 'updated_at'
        ]
        read_only_fields = ['code', 'created_at', 'updated_at']
        
        
        
class FashionModelSerializer3(serializers.ModelSerializer):
    variants = StockVariantForFashionModelsSerializer(many=True, read_only=True)
    images = ModelImageSerializer(many=True, read_only=True)
    total_pieces = serializers.IntegerField(read_only=True)
    available_quantity = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = FashionModel
        fields = [
            'id', 'name', 'code', 'type', 'owner',
            'price_per_piece_for_client', 'price_per_piece_for_dropshipper',
            'description', 'min_pieces_for_dropshipper', 'variants',
            'state', 'promo_code', 'created_at', 'updated_at',
            'images', 'total_pieces', 'available_quantity'
        ]
        
        
