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