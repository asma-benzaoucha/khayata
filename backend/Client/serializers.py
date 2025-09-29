# from rest_framework import serializers
# import json
# from Backendkadi.models.modeles import  FashionModel
# from Backendkadi.models.modeles import ModelImage
# from Backendkadi.models.stock import StockVariant
# from Backendkadi.models.commandes import CustomOrder,CustomOrderImage,Order
# from Backendkadi.models.livraison import  WilayaDelivery
# from Backendkadi.models.user  import User,Client,Couturiere
# from django.contrib.auth import get_user_model
# from Backendkadi.models.socialAccountsLinkgroups import SocialAccountsLinkGroup
# User = get_user_model()


# class StockVariantSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = StockVariant
#         fields = ['color','size','quantity']
              
# class ModelImageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ModelImage
#         fields = ['image']

# class FashionModelSerializer(serializers.ModelSerializer):#with totalsales
#     images = ModelImageSerializer(many=True, read_only=True, source='images.all')
#     total_sales = serializers.SerializerMethodField()
#     sizes = serializers.SerializerMethodField()
#     selection_type = serializers.SerializerMethodField()

#     class Meta:
#         model = FashionModel
#         fields = ['name', 'price_per_piece_for_client', 'images', 'total_sales', 'sizes','selection_type']

#     def get_total_sales(self, obj):
#         # Compter les commandes avec state='done' pour ce modèle
#         return obj.orders.filter(state='done').count()


#     def get_selection_type(self, obj):
#         # Cette méthode sera appelée pour chaque objet sérialisé
#         # On utilise le contexte pour savoir si l'objet était dans les tops ou aléatoire
#         return self.context.get('selection_types', {}).get(obj.id, 'unknown')
    
    
#     def get_sizes(self, obj):
#         # Récupérer les tailles disponibles pour ce modèle
#         return list(obj.variants.values_list('size', flat=True).distinct())


# class CouturiereInfoSerializer(serializers.ModelSerializer):
#     full_name = serializers.CharField(source='user.full_name')
#     email = serializers.CharField(source='user.email')
    
#     class Meta:
#         model = Couturiere
#         fields = ['full_name', 'address', 'phone_number', 'email']

# class FashionModelSerializer2(serializers.ModelSerializer):
#     images = ModelImageSerializer(many=True, read_only=True, source='images.all')
#     sizes = serializers.SerializerMethodField()
#     colors = serializers.SerializerMethodField()
#     variants = StockVariantSerializer(many=True, read_only=True)  # Utilisation du sérialiseur dédié
#     owner_info = serializers.SerializerMethodField()
    
#     class Meta:
#         model = FashionModel
#         fields = ['name', 'price_per_piece_for_client', 'price_per_piece_for_dropshipper','min_pieces_for_dropshipper','images', 'sizes', 'description', 'code', 'colors', 'variants','owner_info','state','type']
    
#     def get_sizes(self, obj):
#         variants = obj.variants.all()
#         sizes = set(variant.size for variant in variants if variant.size)
#         return list(sizes)
    
#     def get_colors(self, obj):
#         variants = obj.variants.all()
#         colors = set(variant.color for variant in variants if variant.color)
#         return list(colors)
    
    
#     def get_owner_info(self, obj):
#         # Si l'owner existe et n'est pas null
#         if obj.owner:
#             try:
#                 # Récupérer le profil couturière associé à l'utilisateur
#                 couturiere_profile = Couturiere.objects.get(user=obj.owner)
#                 return CouturiereInfoSerializer(couturiere_profile).data
#             except Couturiere.DoesNotExist:
#                 # Si le profil couturière n'existe pas, retourner les infos de base de l'user
#                 return {
#                     'full_name': obj.owner.full_name,
#                     'email': obj.owner.email,
#                     'address': None,
#                     'phone_number': None
#                 }
#         # Si owner est null, retourner None
#         return None
    

# # serializers special pour la requete get client orders 
# # OrderImageSerializer deja en haut 
# class CustomOrderImageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomOrderImage
#         fields = ['image']

# class OrderSerializer(serializers.ModelSerializer):
#     model_name = serializers.CharField(source='fashion_model.name', read_only=True)
#     images = serializers.SerializerMethodField()
#     variants = StockVariantSerializer(source='standard_command_details', many=True, read_only=True)
#     total_quantity = serializers.SerializerMethodField()
#     final_price = serializers.SerializerMethodField()

#     class Meta:
#         model = Order
#         fields = [
#             'id', 'model_name', 'final_price', 'phone_number', 
#             'variants', 'total_quantity', 'state', 'created_at', 'images'
#         ]

#     def get_images(self, obj):
#         images = ModelImage.objects.filter(fashion_model=obj.fashion_model)
#         return ModelImageSerializer(images, many=True).data

#     def get_total_quantity(self, obj):
#         return sum(variant.quantity for variant in obj.standard_command_details.all())

#     def get_final_price(self, obj):
#         base_price = obj.fashion_model.price_per_piece_for_client
#         discount = (obj.promo_code.discount_percentage / 100) if obj.promo_code else 0
#         delivery_price = obj.wilaya.delivery_price if obj.wilaya else 0
        
#         total_price = (base_price * (1 - discount)) + delivery_price
#         return round(total_price, 2)

# class CustomOrderSerializer(serializers.ModelSerializer):
#     images = serializers.SerializerMethodField()
#     variants = StockVariantSerializer(source='command_details', many=True, read_only=True)
#     total_quantity = serializers.SerializerMethodField()

#     class Meta:
#         model = CustomOrder
#         fields = [
#             'id', 'nameorder', 'numTelephone', 'initial_price',
#             'variants', 'total_quantity', 'state', 'created_at', 'images'
#         ]

#     def get_images(self, obj): #normalement c'est récuperer directement depuis la relation inverse custum_images
#        # Utilisation de la relation inverse custom_images définie dans le modèle
#         return CustomOrderImageSerializer(obj.custom_images.all(), many=True).data

#     def get_total_quantity(self, obj):
#         return sum(variant.quantity for variant in obj.command_details.all())

    



# class ClientSignupSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField(write_only=True)
#     full_name = serializers.CharField(max_length=255, write_only=True)
#     password = serializers.CharField(write_only=True, style={'input_type': 'password'})
#     password_confirm = serializers.CharField(write_only=True, style={'input_type': 'password'})
#     agreed_to_policy = serializers.BooleanField(write_only=True)

#     class Meta:
#         model = Client
#         fields = ['email', 'full_name', 'password', 'password_confirm', 'agreed_to_policy']

#     def validate(self, attrs):
#         # Vérifier que les mots de passe correspondent
#         if attrs['password'] != attrs['password_confirm']:
#             raise serializers.ValidationError({"password": "Les mots de passe ne correspondent pas."})
        
#         # Vérifier l'acceptation de la politique
#         if not attrs['agreed_to_policy']:
#             raise serializers.ValidationError({"agreed_to_policy": "Vous devez accepter la politique de confidentialité."})
        
#         # Vérifier si l'email existe déjà
#         if User.objects.filter(email=attrs['email']).exists():
#             existing_user = User.objects.get(email=attrs['email'])
#             if existing_user.is_active:
#                 raise serializers.ValidationError({"email": "Un compte avec cet email existe déjà."})
        
#         return attrs

#     def create(self, validated_data):
#         email = validated_data.pop('email')
#         full_name = validated_data.pop('full_name')
#         password = validated_data.pop('password')
#         validated_data.pop('password_confirm')  # On ne conserve pas la confirmation
#         agreed_to_policy = validated_data.pop('agreed_to_policy')

#         try:
#             # Vérifier si l'utilisateur existe déjà mais n'est pas activé
#             existing_user = User.objects.get(email=email)
            
#             if not existing_user.is_active:
#                 # Mettre à jour l'utilisateur existant
#                 existing_user.full_name = full_name
#                 existing_user.role = 'client'
#                 existing_user.set_password(password)
#                 existing_user.generate_email_verification()
#                 existing_user.save()
                
#                 # Mettre à jour ou créer le client
#                 client, created = Client.objects.update_or_create(
#                     user=existing_user,
#                     defaults={'agreed_to_policy': agreed_to_policy}
#                 )
                
#                 return client
#             else:
#                 # Normalement, cette situation est déjà gérée dans validate()
#                 raise serializers.ValidationError({"email": "Un compte avec cet email existe déjà."})
                
#         except User.DoesNotExist:
#             # Créer un nouvel utilisateur
#             user = User.objects.create_user(
#                 email=email,
#                 full_name=full_name,
#                 role='client',
#                 password=password,
#                 is_active=False
#             )
#             user.generate_email_verification()
#             user.save()
            
#             # Créer le client associé
#             client = Client.objects.create(
#                 user=user,
#                 agreed_to_policy=agreed_to_policy
#             )
            
#             return client

# class WilayaDeliverySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = WilayaDelivery
#         fields = ['wilaya_name', 'delivery_price']
        
        







# # pour la requete post enregistrer une commande personalisé :

# class StockVariantSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = StockVariant
#         fields = ['size', 'quantity']


# class CustomOrderSerializer2(serializers.ModelSerializer):
#     images = CustomOrderImageSerializer(many=True, required=False)
#     variants = serializers.CharField(write_only=True)
#     wilaya_name = serializers.CharField(write_only=True)
    
#     class Meta:
#         model = CustomOrder
#         fields = [
#             'nameorder', 'description', 'deadline', 'numTelephone',
#             'wilaya', 'exactaddress', 'command_type', 'model_type',
#             'images', 'variants', 'wilaya_name'
#         ]
#         read_only_fields = ['wilaya']
    
#     def validate_wilaya_name(self, value):
#         """
#         Valide que la wilaya existe et retourne l'instance WilayaDelivery
#         """
#         try:
#             # Recherche insensible à la casse et aux accents
#             wilaya = WilayaDelivery.objects.get(wilaya_name__iexact=value)
#             return wilaya
#         except WilayaDelivery.DoesNotExist:
#             raise serializers.ValidationError(f"Wilaya '{value}' non trouvée")
    
#     def validate_variants(self, value):
#         try:
#             variants_data = json.loads(value)
#             for variant in variants_data:
#                 if 'size' not in variant or 'quantity' not in variant:
#                     raise serializers.ValidationError("Chaque variant doit avoir size et quantity")
#                 if variant['quantity'] <= 0:
#                     raise serializers.ValidationError("La quantité doit être positive")
#             return variants_data
#         except json.JSONDecodeError:
#             raise serializers.ValidationError("Format JSON invalide pour variants")
    
#     def create(self, validated_data):
#         # Extraire les données
#         images_data = self.context['request'].FILES.getlist('images')
#         variants_data = validated_data.pop('variants', [])
#         wilaya_instance = validated_data.pop('wilaya_name')  # ← Déjà une instance WilayaDelivery
        
#         # Créer la commande
#         order = CustomOrder.objects.create(
#             **validated_data,
#             wilaya=wilaya_instance,  # ← Instance correcte
#             user=self.context['request'].user
#         )
        
#         # Créer les images
#         for image_file in images_data:
#             CustomOrderImage.objects.create(
#                 fashion_model=order,
#                 image=image_file
#             )
        
#         # Créer les variants et les associer
#         for variant_data in variants_data:
#           variant = StockVariant.objects.filter(
#            size=variant_data['size'],
#            quantity=variant_data['quantity']
#           ).first()

#         if not variant:
#             variant = StockVariant.objects.create(
#             size=variant_data['size'],
#             quantity=variant_data['quantity']
#         )

#         order.command_details.add(variant)
        
#         return order
    
    


# class SocialAccountsLinkGroupSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SocialAccountsLinkGroup
#         fields = [
#             'id',
#             'whatsapp',
#             'instagram',
#             'facebook',
#             'group_dropshipping',
#             'group_investissement',
#             'created_at',
#             'updated_at'
#         ]
#         read_only_fields = ['id', 'created_at', 'updated_at']
        
        
               
        
from rest_framework import serializers
import json
from Backendkadi.models.modeles import  FashionModel
from Backendkadi.models.modeles import ModelImage
from Backendkadi.models.stock import StockVariantForCommands,StockVariantForFashionModels
from Backendkadi.models.commandes import CustomOrder,CustomOrderImage,Order
from Backendkadi.models.livraison import  WilayaDelivery
from Backendkadi.models.user  import User,Client,Couturiere
from django.contrib.auth import get_user_model
from Backendkadi.models.socialAccountsLinkgroups import SocialAccountsLinkGroup
User = get_user_model()


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
    images = ModelImageSerializer(many=True, read_only=True, source='images.all')
    total_sales = serializers.SerializerMethodField()
    sizes = serializers.SerializerMethodField()
    selection_type = serializers.SerializerMethodField()
    variants = StockVariantForFashionModelsSerializer(many=True, read_only=True)

    class Meta:
        model = FashionModel
        fields = ['name', 'price_per_piece_for_client', 'images', 'total_sales', 'sizes', 'selection_type', 'variants']

    def get_total_sales(self, obj):
        # Compter les commandes avec state='done' pour ce modèle
        return obj.orders.filter(state='done').count()

    def get_selection_type(self, obj):
        return self.context.get('selection_types', {}).get(obj.id, 'unknown')
    
    def get_sizes(self, obj):
        # Récupérer les tailles disponibles pour ce modèle depuis les variantes liées
        return list(obj.variants.values_list('size', flat=True).distinct())


class CouturiereInfoSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='user.full_name')
    email = serializers.CharField(source='user.email')
    
    class Meta:
        model = Couturiere
        fields = ['full_name', 'address', 'phone_number', 'email']

class FashionModelSerializer2(serializers.ModelSerializer):
    images = ModelImageSerializer(many=True, read_only=True, source='images.all')
    sizes = serializers.SerializerMethodField()
    colors = serializers.SerializerMethodField()
    variants = StockVariantForFashionModelsSerializer(many=True, read_only=True)  # Utilisation du sérialiseur dédié
    owner_info = serializers.SerializerMethodField()
    
    class Meta:
        model = FashionModel
        fields = ['name', 'price_per_piece_for_client', 'price_per_piece_for_dropshipper','min_pieces_for_dropshipper','images', 'sizes', 'description', 'code', 'colors', 'variants','owner_info','state','type']
    
    def get_sizes(self, obj):
        variants = obj.variants.all()
        sizes = set(variant.size for variant in variants if variant.size)
        return list(sizes)
    
    def get_colors(self, obj):
        variants = obj.variants.all()
        colors = set(variant.color for variant in variants if variant.color)
        return list(colors)
    
    
    def get_owner_info(self, obj):
        # Si l'owner existe et n'est pas null
        if obj.owner:
            try:
                # Récupérer le profil couturière associé à l'utilisateur
                couturiere_profile = Couturiere.objects.get(user=obj.owner)
                return CouturiereInfoSerializer(couturiere_profile).data
            except Couturiere.DoesNotExist:
                # Si le profil couturière n'existe pas, retourner les infos de base de l'user
                return {
                    'full_name': obj.owner.full_name,
                    'email': obj.owner.email,
                    'address': None,
                    'phone_number': None
                }
        # Si owner est null, retourner None
        return None
    

# serializers special pour la requete get client orders 
# OrderImageSerializer deja en haut 
class CustomOrderImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomOrderImage
        fields = ['image']

class OrderSerializer(serializers.ModelSerializer):
    model_name = serializers.CharField(source='fashion_model.name', read_only=True)
    images = serializers.SerializerMethodField()
    variants = StockVariantForCommandsSerializer(source='standard_command_details', many=True, read_only=True)
    total_quantity = serializers.SerializerMethodField()
    final_price = serializers.SerializerMethodField()
    pricewilaya=serializers.SerializerMethodField()
    dropshipper_client_name = serializers.SerializerMethodField()


    class Meta:
        model = Order
        fields = [
            'id', 'model_name', 'final_price', 'phone_number', 
            'variants', 'total_quantity', 'state', 'created_at', 'images','pricewilaya','dropshipper_client_name'
        ]
        
        
    def get_dropshipper_client_name(self, obj):
        # Retourne le nom du client dropshipper si la commande en a un
        if obj.dropshipper_client:
            return obj.dropshipper_client.nom_client
        return None
    
    
    def get_images(self, obj):
        images = ModelImage.objects.filter(fashion_model=obj.fashion_model)
        return ModelImageSerializer(images, many=True).data

    def get_total_quantity(self, obj):
        return sum(variant.quantity for variant in obj.standard_command_details.all())
    
    def get_pricewilaya(self, obj):
        return(obj.wilaya.delivery_price if obj.wilaya else 0) 

    def get_final_price(self, obj):
       # Vérifier si la commande a un dropshipper
       if obj.dropshipper_client:
          base_price = obj.fashion_model.price_per_piece_for_dropshipper
       else:
          base_price = obj.fashion_model.price_per_piece_for_client
    
       discount = (obj.promo_code.discount_percentage / 100) if obj.promo_code else 0
    
       total_price = (base_price * (1 - discount)) 
       return round(total_price, 2)
        
        
       

class CustomOrderSerializer(serializers.ModelSerializer):
    pricewilaya=serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    variants = StockVariantForCommandsSerializer(source='command_details', many=True, read_only=True)
    total_quantity = serializers.SerializerMethodField()

    class Meta:
        model = CustomOrder
        fields = [
            'id', 'nameorder', 'numTelephone', 'initial_price',
            'variants', 'total_quantity', 'state', 'created_at', 'images','pricewilaya'
        ]

    def get_images(self, obj): #normalement c'est récuperer directement depuis la relation inverse custum_images
       # Utilisation de la relation inverse custom_images définie dans le modèle
        return CustomOrderImageSerializer(obj.custom_images.all(), many=True).data
    
    def get_pricewilaya(self, obj):
        return(obj.wilaya.delivery_price if obj.wilaya else 0) 
    
    def get_total_quantity(self, obj):
        return sum(variant.quantity for variant in obj.command_details.all())

    



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
        
        







# pour la requete post enregistrer une commande personalisé :




class CustomOrderSerializer2(serializers.ModelSerializer):
    images = CustomOrderImageSerializer(many=True, required=False)
    variants = serializers.CharField(write_only=True)
    wilaya_name = serializers.CharField(write_only=True)
    
    class Meta:
        model = CustomOrder
        fields = [
            'nameorder', 'description', 'deadline', 'numTelephone',
            'wilaya', 'exactaddress', 'command_type', 'model_type',
            'images', 'variants', 'wilaya_name'
        ]
        read_only_fields = ['wilaya']
    
    def validate_wilaya_name(self, value):
        """
        Valide que la wilaya existe et retourne l'instance WilayaDelivery
        """
        try:
            # Recherche insensible à la casse et aux accents
            wilaya = WilayaDelivery.objects.get(wilaya_name__iexact=value)
            return wilaya
        except WilayaDelivery.DoesNotExist:
            raise serializers.ValidationError(f"Wilaya '{value}' non trouvée")
    
    def validate_variants(self, value):
        try:
            variants_data = json.loads(value)
            for variant in variants_data:
                if 'size' not in variant or 'quantity' not in variant:
                    raise serializers.ValidationError("Chaque variant doit avoir size et quantity")
                if variant['quantity'] <= 0:
                    raise serializers.ValidationError("La quantité doit être positive")
            return variants_data
        except json.JSONDecodeError:
            raise serializers.ValidationError("Format JSON invalide pour variants")
    
    def create(self, validated_data):
        # Extraire les données
        images_data = self.context['request'].FILES.getlist('images')
        variants_data = validated_data.pop('variants', [])
        wilaya_instance = validated_data.pop('wilaya_name')  # ← Déjà une instance WilayaDelivery
        
        # Créer la commande
        order = CustomOrder.objects.create(
            **validated_data,
            wilaya=wilaya_instance,  # ← Instance correcte
            user=self.context['request'].user
        )
        
        # Créer les images
        for image_file in images_data:
            CustomOrderImage.objects.create(
                fashion_model=order,
                image=image_file
            )
        
        # Créer les variants et les associer
        for variant_data in variants_data:
          variant = StockVariantForCommands.objects.filter(
           size=variant_data['size'],
           quantity=variant_data['quantity']
          ).first()

          if not variant:
            variant = StockVariantForCommands.objects.create(
            size=variant_data['size'],
            quantity=variant_data['quantity']
           )

          order.command_details.add(variant)
        
        return order
    
    


class SocialAccountsLinkGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialAccountsLinkGroup
        fields = [
            'id',
            'whatsapp',
            'instagram',
            'facebook',
            'group_dropshipping',
            'group_investissement',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']