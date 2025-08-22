from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from .models import Couturiere, User ,Dropshipper ,UserDocuments
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer




class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['full_name', 'email', 'password']  

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

class CouturiereSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Couturiere
        fields = ['user', 'address','phone_number', 'agreed_to_policy']

    def validate_agreed_to_policy(self, value):
        if value is not True:
            raise serializers.ValidationError("Vous devez accepter les conditions d'utilisation.")
        return value


    def create(self, validated_data):
        user_data = validated_data.pop('user')
        email = user_data['email']

        try:
            existing_user = User.objects.get(email=email)
            if existing_user.is_active:
                raise serializers.ValidationError("Cet email est déjà utilisé.")
            else:
                # Écrase les anciennes données
                existing_user.full_name = user_data['full_name']
                existing_user.role = 'couturiere'
                existing_user.generate_email_verification()
                existing_user.set_password(user_data['password'])
                existing_user.save()
                return Couturiere.objects.create(user=existing_user, **validated_data)
        except User.DoesNotExist:
            # Nouvel utilisateur
            user = User(**user_data)
            user.role = 'couturiere'
            user.is_active = False
            user.generate_email_verification()
            user.set_password(user_data['password'])
            user.save()
            return Couturiere.objects.create(user=user, **validated_data)
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
                                                                                                                                                            
        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError("Email ou mot de passe incorrect.")
        if not user.is_active:
            raise serializers.ValidationError("Ce compte est inactif.")

        # 🔍 Vérification du rôle et de l'acceptation
        if user.role == "couturiere":
            try:
                couturiere = Couturiere.objects.get(user=user)
                if not couturiere.is_accepted:
                    raise serializers.ValidationError("Votre compte couturière est en attente de validation.")
            except Couturiere.DoesNotExist:
                raise serializers.ValidationError("Compte couturière introuvable.")

        elif user.role == "dropshipper":
            try:
                dropshipper = Dropshipper.objects.get(user=user)
                if not dropshipper.is_accepted:
                    raise serializers.ValidationError("Votre compte dropshipper est en attente de validation.")
            except Dropshipper.DoesNotExist:
                raise serializers.ValidationError("Compte dropshipper introuvable.")

        data['user'] = user
        return data
    
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

        if not user.is_active and user.email_verification_token is None :
            raise serializers.ValidationError({
        "error_type": "account_disabled",
        "detail": "Votre compte a été désactivé par l'administration."
    })

        # Vérifications personnalisées (Couturiere/Dropshipper)
        if user.role == "couturiere":
            try:
                couturiere = Couturiere.objects.get(user=user)
                if not couturiere.is_accepted:
                    raise serializers.ValidationError( {
                        "error_type": "couturiere_pending",
                        "detail":"Votre compte couturière est en attente de validation.",
})
            except Couturiere.DoesNotExist:
                raise serializers.ValidationError({
                    "error_type": "couturière_not_found",
                    "detail": "Compte couturière introuvable."
                })
        elif user.role == "dropshipper":
            try:
                dropshipper = Dropshipper.objects.get(user=user)
                if not dropshipper.is_accepted:
                    raise serializers.ValidationError({
                        "error_type": "dropshipper_pending",
                        "detail": "Votre compte dropshipper est en attente de validation."
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
        


