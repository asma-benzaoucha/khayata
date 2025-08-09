
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
    
    
    
    #hadi chi
# class CouturiereSignupView(APIView):
#     parser_classes = [MultiPartParser, FormParser]#hna bah nakhdam b form_data f cote postman psq les types des inputs contient file type

#     def post(self, request):
#         serializer = CouturiereSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             send_verification_email(user)
#             return Response({"message": "Email de vérification envoyé."}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)













# #hadi taliya li commentitha 9bal  jdida lirahi khadama
# class ResetPasswordView(APIView):
#     def post(self, request):
#         reset_token = request.data.get("reset_token")
#         new_password = request.data.get("new_password")

#         if not all([reset_token, new_password]):
#             return Response({"detail": "البيانات غير مكتملة."}, status=400)

#         try:
#             data = signing.loads(reset_token, salt="final-password-reset", max_age=600)
#             email = data["email"]
#         except signing.SignatureExpired:
#             return Response({"detail": "انتهت صلاحية الرابط."}, status=400)
#         except signing.BadSignature:
#             return Response({"detail": "رمز غير صالح."}, status=400)

#         try:
#             user = User.objects.get(email=email)
#         except User.DoesNotExist:
#             return Response({"detail": "المستخدم غير موجود."}, status=404)

#         user.set_password(new_password)
#         user.save()
#         print(user.password)  # Doit montrer un nouveau hash
#         RefreshToken.for_user(user).blacklist() 
#         return Response({"detail": "تم إعادة تعيين كلمة المرور بنجاح."})
