from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from .models import Couturiere, User ,Dropshipper ,UserDocuments,StockVariantForFashionModels,FashionModel,ModelImage,CustomOrder,CustomOrderImage
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password



class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['full_name', 'email', 'password']  

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

# class CouturiereSerializer(serializers.ModelSerializer):
#     user = UserSerializer()

#     class Meta:
#         model = Couturiere
#         fields = ['user', 'address','phone_number', 'agreed_to_policy']

#     def validate_agreed_to_policy(self, value):
#         if value is not True:
#             raise serializers.ValidationError("Vous devez accepter les conditions d'utilisation.")
#         return value


#     def create(self, validated_data):
#         user_data = validated_data.pop('user')
#         email = user_data['email']

#         try:
#             existing_user = User.objects.get(email=email)
#             if existing_user.is_active:
#                 raise serializers.ValidationError("Cet email est déjà utilisé.")
#             else:
#                 # Écrase les anciennes données
#                 existing_user.full_name = user_data['full_name']
#                 existing_user.role = 'couturiere'
#                 existing_user.generate_email_verification()
#                 existing_user.set_password(user_data['password'])
#                 existing_user.save()
#                 return Couturiere.objects.create(user=existing_user, **validated_data)
#         except User.DoesNotExist:
#             # Nouvel utilisateur
#             user = User(**user_data)
#             user.role = 'couturiere'
#             user.is_active = False
#             user.generate_email_verification()
#             user.set_password(user_data['password'])
#             user.save()
#             return Couturiere.objects.create(user=user, **validated_data)
    
# class LoginSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     password = serializers.CharField(write_only=True)

#     def validate(self, data):
#         email = data.get('email')
#         password = data.get('password')
                                                                                                                                                            
#         user = authenticate(email=email, password=password)

#         if user is None:
#             raise serializers.ValidationError("Email ou mot de passe incorrect.")
#         if not user.is_active:
#             raise serializers.ValidationError("Ce compte est inactif.")

#         # 🔍 Vérification du rôle et de l'acceptation
#         if user.role == "couturiere":
#             try:
#                 couturiere = Couturiere.objects.get(user=user)
#                 if not couturiere.is_accepted:
#                     raise serializers.ValidationError("Votre compte couturière est en attente de validation.")
#             except Couturiere.DoesNotExist:
#                 raise serializers.ValidationError("Compte couturière introuvable.")

#         elif user.role == "dropshipper":
#             try:
#                 dropshipper = Dropshipper.objects.get(user=user)
#                 if not dropshipper.is_accepted:
#                     raise serializers.ValidationError("Votre compte dropshipper est en attente de validation.")
#             except Dropshipper.DoesNotExist:
#                 raise serializers.ValidationError("Compte dropshipper introuvable.")

#         data['user'] = user
#         return data
    
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({
                "error_type": "bad_email_or_password",
                "detail": "Email ou mot de passe incorrect."
            })

        if not user.check_password(password):
            raise serializers.ValidationError({
                "error_type": "bad_email_or_password",
                "detail": "Email ou mot de passe incorrect."
            })

        if user.email_verification_token is not None and not user.is_active:
            raise serializers.ValidationError({
                "error_type": "inactive_account",
                "detail": "Veuillez vérifier votre adresse email."
            })
        
        
        if user.role not in ["couturiere", "dropshipper"]:
           if not user.is_active and user.email_verification_token is None:
            raise serializers.ValidationError({
        "error_type": "account_disabled",
        "detail": "Votre compte a été désactivé par l'administration."
           })
 
        # Vérifications personnalisées (Couturiere/Dropshipper)
        if user.role == "couturiere":
            try:
                couturiere = Couturiere.objects.get(user=user)
                
                
                if couturiere.is_accepted ==None :
                    raise serializers.ValidationError( {
                        "error_type": "couturiere_pending",
                        "detail":"Votre compte couturière est en attente de validation.",  
              })
                
                if couturiere.is_accepted ==False :
                    raise serializers.ValidationError( {
                        "error_type": "couturiere_refused",
                        "detail":"Votre compte couturière est refusé par l'administrateur.",
                
              })
                
                if couturiere.is_accepted ==True and  user.is_active==False:
                    raise serializers.ValidationError( {
                        "error_type": "couturiere_désactivé",
                        "detail":"Votre compte couturière est désactivé par l'administrateur.",
                
              }) 
                        
            except Couturiere.DoesNotExist:
                raise serializers.ValidationError({
                    "error_type": "couturière_not_found",
                    "detail": "Compte couturière introuvable."
                })
        elif user.role == "dropshipper":
            try:
                dropshipper = Dropshipper.objects.get(user=user)
                if dropshipper.is_accepted ==None:
                    raise serializers.ValidationError({
                        "error_type": "dropshipper_pending",
                        "detail": "Votre compte dropshipper est en attente de validation."
                    })
                    
                if dropshipper.is_accepted ==False :
                    raise serializers.ValidationError( {
                        "error_type": "dropshipper_refused",
                        "detail":"Votre compte dropshipper est refusé par l'administrateur.",
                
              })
                    
                if dropshipper.is_accepted ==True and  user.is_active==False:
                    raise serializers.ValidationError( {
                        "error_type": "dropshipper_désactivé",
                        "detail":"Votre compte dropshipper est désactivé par l'administrateur.",
                
              })
            except Dropshipper.DoesNotExist:
                raise serializers.ValidationError({
                    "error_type": "dropshipper_not_found",
                    "detail": "Compte dropshipper introuvable."
                })
        # Générer le Token JWT (Access + Refresh)
        data = super().validate(attrs)

        # Ajouter des infos utilisateur personnalisées dans la réponse
        data['user'] = {
            'id': user.id,
            'email': user.email,
            'full_name': user.full_name,
            'role': user.role,
        }
        return data


class UserDocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDocuments
        fields = ['id', 'nom', 'user']
        read_only_fields = ['id']


class CouturiereSerializer(serializers.ModelSerializer):
    documents = UserDocumentsSerializer(many=True, read_only=True, source='user.documents')
    
    class Meta:
        model = Couturiere
        fields = '__all__'


class CouturiereSignupSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    documents = serializers.ListField(
        child=serializers.FileField(max_length=100000),
        write_only=True,
        required=False,
        max_length=5  # Limite à 5 fichiers
    )

    class Meta:
        model = Couturiere
        fields = ['user', 'address', 'phone_number', 'agreed_to_policy', 'documents']

    def validate_agreed_to_policy(self, value):
        if value is not True:
            raise serializers.ValidationError("Vous devez accepter les conditions d'utilisation.")
        return value

    def validate_documents(self, value):
        if len(value) > 5:
            raise serializers.ValidationError("Maximum 5 fichiers autorisés.")
        return value

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        documents = validated_data.pop('documents', [])
        email = user_data['email']

        try:
            existing_user = User.objects.get(email=email)
            if existing_user.is_active:
                raise serializers.ValidationError("Cet email est déjà utilisé.")
            else:
                # Mise à jour de l'utilisateur existant
                existing_user.full_name = user_data['full_name']
                existing_user.role = 'couturiere'
                existing_user.generate_email_verification()
                existing_user.set_password(user_data['password'])
                existing_user.save()
                
                couturiere, _ = Couturiere.objects.update_or_create(
                    user=existing_user,
                    defaults=validated_data
                )
                
                # Suppression des anciens documents
                existing_user.documents.all().delete()
                
                # Création des nouveaux documents
                for doc in documents:
                    UserDocuments.objects.create(
                        nom=doc,
                        user=existing_user
                    )
                
                return couturiere
                
        except User.DoesNotExist:
            # Nouvel utilisateur
            user = User.objects.create(
                email=email,
                full_name=user_data['full_name'],
                role='couturiere',
                is_active=False
            )
            user.generate_email_verification()
            user.set_password(user_data['password'])
            user.save()
            
            couturiere = Couturiere.objects.create(
                user=user,
                **validated_data
            )
            
            # Création des documents
            for doc in documents:
                UserDocuments.objects.create(
 
                    nom=doc,
                    user=user
                )
            
            return couturiere    




class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        write_only=True, 
        required=True,
        style={'input_type': 'password'}
    )
    newPassword = serializers.CharField(
        write_only=True, 
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )

    def validate_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("الرقم السري الحالي الذي أدخلته خاطئ ")
        return value
    
    
    
    










class StockVariantForFashionModelsSerializer(serializers.ModelSerializer):
    hex = serializers.SerializerMethodField()

    class Meta:
        model = StockVariantForFashionModels
        fields = ["id", "size", "color", "quantity", "hex"]

    def get_hex(self, obj):
        try:
            return CSS3_NAMES_TO_HEX[obj.color.lower()]
        except KeyError:
            return "#cccccc"


class CouturiereModelSerializer(serializers.ModelSerializer):
    variants = serializers.JSONField(write_only=True)
    files = serializers.ListField(
        child=serializers.FileField(max_length=100000),
        write_only=True,
        required=True,
        max_length=5  
    )

    class Meta:
        model = FashionModel
        fields = ['type', 'name', 'description', 'price_per_piece_for_client', 'files','variants']
        read_only_fields = ["code","owner", "created_at", "updated_at"]


    def validate_files(self, value):
        if len(value) > 5:
            raise serializers.ValidationError("Maximum 5 fichiers autorisés.")
        return value

    def create(self, validated_data):
        request = self.context.get("request")  # on récupère la requête
        documents = validated_data.pop('files', [])

        user = request.user                   # récupère l'utilisateur du JWT
        # récupérer variants du validated_data
        variants_data = validated_data.pop('variants')

        # ✅ Tout est dans une transaction
        with transaction.atomic():
            # Créer le FashionModel
            fashion_model = FashionModel.objects.create(owner=user, **validated_data)

            # Créer les variantes + relation
            for variant_data in variants_data:
                StockVariantForFashionModels.objects.create(
                    fashion_model=fashion_model,
                    **{**variant_data, "quantity": 1}  # quantity forcé à 1
                    )

                
            for doc in documents:
                ModelImage.objects.create(
                    image=doc,
                    fashion_model=fashion_model
                )
                
        return fashion_model

class ModelFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelImage
        fields = ['id', 'image', 'fashion_model']
        read_only_fields = ['id']

class FashionModelListSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    status = serializers.CharField(source='state')
    total_pieces = serializers.SerializerMethodField()
    created_date = serializers.SerializerMethodField()
    variants = StockVariantForFashionModelsSerializer(many=True, read_only=True)

    class Meta:
        model = FashionModel
        fields = [
            'id', 'name', 'code', 'type', 'price_per_piece_for_client',
            'description', 'status', 'created_date', 'images',
            'total_pieces', 'variants'
        ]

    def get_images(self, obj):
        request = self.context.get('request')
        images = obj.images.all()
        if images and request:
            return [request.build_absolute_uri(image.image.url) for image in images]
        elif images:
            return [request.build_absolute_uri(image.image.url) for image in images]
        return []

    def get_total_pieces(self, obj):
        return obj.total_pieces()

    def get_created_date(self, obj):
        return obj.created_at.strftime("%Y-%m-%d")

class CustomOrderImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomOrderImage
        fields = ["id", "image"]




from .models import StockVariantForCommands
class StockVariantForCommandsSerializer(serializers.ModelSerializer):
    hex = serializers.SerializerMethodField()

    class Meta:
        model = StockVariantForCommands
        fields = ["id", "size", "color", "quantity","hex"]
        

    def get_hex(self, obj):
        try:
            return CSS3_NAMES_TO_HEX[obj.color.lower()]
        except KeyError:
            return "#cccccc"


class CustomOrderSerializer(serializers.ModelSerializer):
    custom_images = CustomOrderImageSerializer(many=True, read_only=True)
    variants = StockVariantForCommandsSerializer(
        source="command_details", many=True, read_only=True
    )

    # state = serializers.CharField(source='state')
    total_requested_quantity = serializers.SerializerMethodField()
    created_date = serializers.SerializerMethodField()
    
    class Meta:

        model = CustomOrder
        fields = [
            "id", "nameorder", "codeorder", "numTelephone", "exactaddress",
            "initial_price", "command_type", "model_type", "deadline",
            "description", "state",  "updated_at",
            "custom_images","variants","total_requested_quantity","created_date"
        ]
        


    def get_custom_images(self, obj):
        request = self.context.get('request')
        images = obj.images.all()
        if images and request:
            return [request.build_absolute_uri(image.image.url) for image in images]
        elif images:
            return [request.build_absolute_uri(image.image.url) for image in images]
        return []

    def get_total_requested_quantity(self, obj):
        return obj.total_requested_quantity()

    def get_created_date(self, obj):
        return obj.created_at.strftime("%Y-%m-%d")












# accounts/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Couturiere

User = get_user_model()

class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "full_name", "email", "role", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

    def update(self, instance, validated_data):
        email = validated_data.get("email")
        if email and email != instance.email:
            instance.email = email
        return super().update(instance, validated_data)


class CouturiereAccountSerializer(serializers.ModelSerializer):
    user = UserAccountSerializer(read_only=True)

    class Meta:
        model = Couturiere
        fields = ["id", "user", "address", "phone_number", "is_accepted", "agreed_to_policy"]


class CouturiereAccountSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="user.full_name", read_only=False)
    email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Couturiere
        fields = ["id", "full_name", "email", "address", "phone_number", "is_accepted", "agreed_to_policy"]

    def update(self, instance, validated_data):
        # Mise à jour des champs du modèle User
        user_data = validated_data.pop("user", {})
        if "full_name" in validated_data:
            instance.user.full_name = validated_data["full_name"]
            instance.user.save()

        # Mise à jour des champs Couturiere
        instance.address = validated_data.get("address", instance.address)
        instance.phone_number = validated_data.get("phone_number", instance.phone_number)
        instance.save()

        return instance


class AffiliateAccountSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="user.full_name", read_only=False)
    email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = UserAccountSerializer
        fields = ["id", "full_name", "email"]

    def update(self, instance, validated_data):
        # Mise à jour des champs du modèle User
        user_data = validated_data.pop("user", {})
        if "full_name" in validated_data:
            instance.user.full_name = validated_data["full_name"]
            instance.user.save()

        # # Mise à jour des champs Couturiere
        # instance.address = validated_data.get("address", instance.address)
        # instance.phone_number = validated_data.get("phone_number", instance.phone_number)
        # instance.save()

        return instance


# class PasswordChangeSerializer(serializers.Serializer):
#     current_password = serializers.CharField(required=True)
#     new_password = serializers.CharField(required=True)

#     def validate(self, data):
#         user = self.context["request"].user
#         if not user.check_password(data["current_password"]):
#             raise serializers.ValidationError({"current_password": "كلمة المرور غير صحيحة"})
#         return data

#     def save(self, **kwargs):
#         user = self.context["request"].user
#         user.set_password(self.validated_data["new_password"])
#         user.save()
#         return user


class ChangePasswordWithVerificationSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)








from rest_framework import serializers
from .models import PromoCode, FashionModel, User


class FashionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = FashionModel
        fields = ["id", "name", "code", "description", "state"]


class PromoCodeSerializer(serializers.ModelSerializer):
    models_CodePromo = FashionModelSerializer(many=True, read_only=True)
    affiliate_name = serializers.CharField(source="affiliate.full_name", read_only=True)

    class Meta:
        model = PromoCode
        fields = [
            "id",
            "code",
            "affiliate",       # id of affiliate
            "affiliate_name",  # readable affiliate name
            "profit_percentage",
            "discount_percentage",
            "start_date",
            "expiration_date",
            "usage_count",
            "models_CodePromo",   # 🔗 related fashion models
        ]

# serializers.py
from rest_framework import serializers
from .models import User

class AffiliateAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "full_name", "email", "role", "created_at", "updated_at"]
        read_only_fields = ["id", "email", "role", "created_at", "updated_at"]
















# serializers.py
from rest_framework import serializers
from .models import Order

class AffiliateOrderSerializer(serializers.ModelSerializer):
    promo_code = serializers.CharField(source="promo_code.code", read_only=True)
    fashion_model_code = serializers.CharField(source="fashion_model.code", read_only=True)
    quantity = serializers.SerializerMethodField()
    final_price = serializers.SerializerMethodField()
    affiliate_profit = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            "created_at", 
            "promo_code", 
            "fashion_model_code", 
            "quantity", 
            "final_price",
            "affiliate_profit",
        ]

    def get_quantity(self, obj):
        return sum(v.quantity for v in obj.standard_command_details.all())

    def get_final_price(self, obj):
        # Suppose FashionModel has price_per_piece_for_client
        base_price = obj.fashion_model.price_per_piece_for_client * self.get_quantity(obj)
        if obj.promo_code:
            discount = base_price * (obj.promo_code.discount_percentage / 100)
            return base_price - discount
        return base_price

    def get_affiliate_profit(self, obj):
        if obj.promo_code:
            return self.get_final_price(obj) * (obj.promo_code.profit_percentage / 100)
        return 0