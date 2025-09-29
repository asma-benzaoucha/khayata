from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from rest_framework import serializers

from Backendkadi.models.commandes import  CustomOrder 
from Backendkadi.models.user import  User ,Client,Couturiere
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

class DropshipperSignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    full_name = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, style={'input_type': 'password'})
    phone= serializers.CharField(write_only=True)  
    
    class Meta:
        model = Dropshipper
        fields = ['email', 'full_name', 'password', 'password_confirm', 'store_link', 'agreed_to_policy','phone']
    
    def validate_agreed_to_policy(self, value):
        if not value:
            raise serializers.ValidationError("Vous devez accepter les conditions d'utilisation.")
        return value
    
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password_confirm": "Les mots de passe ne correspondent pas."})
        return data
    
    def create(self, validated_data):
        email = validated_data.pop('email')
        full_name = validated_data.pop('full_name')
        password = validated_data.pop('password')
        validated_data.pop('password_confirm', None)  # Remove confirmation field
        phone_number = validated_data.pop('phone')
        validated_data['phone_number'] = phone_number
        
        try:
            # Vérifier si l'utilisateur existe déjà
            existing_user = User.objects.get(email=email)
            
            if existing_user.is_active:
                raise serializers.ValidationError({"email": "Cet email est déjà utilisé."})
            else:
                # Mise à jour de l'utilisateur existant inactif
                existing_user.full_name = full_name
                existing_user.role = 'dropshipper'
                existing_user.generate_email_verification()
                existing_user.set_password(password)
                existing_user.save()
                
                # Mise à jour ou création du profil dropshipper
                dropshipper, created = Dropshipper.objects.update_or_create(
                    user=existing_user,
                    defaults=validated_data
                )
                
                return dropshipper
                
        except User.DoesNotExist:
            # Création d'un nouvel utilisateur
            user = User.objects.create(
                email=email,
                full_name=full_name,
                role='dropshipper',
                is_active=False
            )
            user.generate_email_verification()
            user.set_password(password)
            user.save()
            
            # Création du profil dropshipper
            dropshipper = Dropshipper.objects.create(
                user=user,
                **validated_data
            )
            
            return dropshipper





