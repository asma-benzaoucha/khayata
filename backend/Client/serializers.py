from rest_framework import serializers
from Backendkadi.models.modeles import  FashionModel
from Backendkadi.models.modeles import ModelImage
from Backendkadi.models.stock import StockVariant
from Backendkadi.models.commandes import CustomOrder,CustomOrderImage,Order
from Backendkadi.models.livraison import  WilayaDelivery
from Backendkadi.models.user  import User,Client
from django.contrib.auth import get_user_model
User = get_user_model()

class ModelImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelImage
        fields = ['image']

class FashionModelSerializer(serializers.ModelSerializer):#with totalsales
    images = ModelImageSerializer(many=True, read_only=True, source='images.all')
    total_sales = serializers.SerializerMethodField()
    sizes = serializers.SerializerMethodField()

    class Meta:
        model = FashionModel
        fields = ['name', 'price_per_piece_for_client', 'images', 'total_sales', 'sizes']

    def get_total_sales(self, obj):
        # Compter les commandes avec state='done' pour ce modèle
        return obj.orders.filter(state='done').count()

    def get_sizes(self, obj):
        # Récupérer les tailles disponibles pour ce modèle
        return list(obj.variants.values_list('size', flat=True).distinct())



class FashionModelSerializer2(serializers.ModelSerializer): #without total_sales
    images = ModelImageSerializer(many=True, read_only=True, source='images.all')
    sizes = serializers.SerializerMethodField()
    
    class Meta:
        model = FashionModel
        fields = ['name', 'price_per_piece_for_client', 'images', 'sizes','description','code']
    
    def get_sizes(self, obj):
        # Récupère toutes les tailles disponibles pour ce modèle (uniques)
        variants = obj.variants.all()
        sizes = set(variant.size for variant in variants if variant.size)
        return list(sizes)










class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'full_name', 'email']

class StockVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockVariant
        fields = ['quantity']

class ModelImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelImage
        fields = ['image']

class FashionModelSerializer(serializers.ModelSerializer):
    images = ModelImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = FashionModel
        fields = ['name', 'price_per_piece_for_client', 'images']

class CustomOrderImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomOrderImage
        fields = ['image']

class CustomOrderSerializer(serializers.ModelSerializer):
    custom_images = CustomOrderImageSerializer(many=True, read_only=True)
    command_details = StockVariantSerializer(many=True, read_only=True)
    
    class Meta:
        model = CustomOrder
        fields = ['id', 'created_at', 'numTelephone', 'state', 'nameorder', 
                  'command_type', 'model_type',
                 'deadline', 'description', 'custom_images', 'command_details']

class OrderSerializer(serializers.ModelSerializer):
    fashion_model = FashionModelSerializer(read_only=True)
    standard_command_details = StockVariantSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'created_at', 'phone_number', 'state',
                  'fashion_model', 'standard_command_details', ]





class ClientSignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    full_name = serializers.CharField(max_length=255, write_only=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, style={'input_type': 'password'})
    agreed_to_policy = serializers.BooleanField(write_only=True)

    class Meta:
        model = Client
        fields = ['email', 'full_name', 'password', 'password_confirm', 'agreed_to_policy']

    def validate(self, attrs):
        # Vérifier que les mots de passe correspondent
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Les mots de passe ne correspondent pas."})
        
        # Vérifier l'acceptation de la politique
        if not attrs['agreed_to_policy']:
            raise serializers.ValidationError({"agreed_to_policy": "Vous devez accepter la politique de confidentialité."})
        
        # Vérifier si l'email existe déjà
        if User.objects.filter(email=attrs['email']).exists():
            existing_user = User.objects.get(email=attrs['email'])
            if existing_user.is_active:
                raise serializers.ValidationError({"email": "Un compte avec cet email existe déjà."})
        
        return attrs

    def create(self, validated_data):
        email = validated_data.pop('email')
        full_name = validated_data.pop('full_name')
        password = validated_data.pop('password')
        validated_data.pop('password_confirm')  # On ne conserve pas la confirmation
        agreed_to_policy = validated_data.pop('agreed_to_policy')

        try:
            # Vérifier si l'utilisateur existe déjà mais n'est pas activé
            existing_user = User.objects.get(email=email)
            
            if not existing_user.is_active:
                # Mettre à jour l'utilisateur existant
                existing_user.full_name = full_name
                existing_user.role = 'client'
                existing_user.set_password(password)
                existing_user.generate_email_verification()
                existing_user.save()
                
                # Mettre à jour ou créer le client
                client, created = Client.objects.update_or_create(
                    user=existing_user,
                    defaults={'agreed_to_policy': agreed_to_policy}
                )
                
                return client
            else:
                # Normalement, cette situation est déjà gérée dans validate()
                raise serializers.ValidationError({"email": "Un compte avec cet email existe déjà."})
                
        except User.DoesNotExist:
            # Créer un nouvel utilisateur
            user = User.objects.create_user(
                email=email,
                full_name=full_name,
                role='client',
                password=password,
                is_active=False
            )
            user.generate_email_verification()
            user.save()
            
            # Créer le client associé
            client = Client.objects.create(
                user=user,
                agreed_to_policy=agreed_to_policy
            )
            
            return client






class WilayaDeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = WilayaDelivery
        fields = ['wilaya_name', 'delivery_price']