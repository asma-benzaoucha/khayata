from django.utils import timezone
from django.utils.http import urlsafe_base64_decode
from django.core import signing
from django.core.mail import send_mail
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from rest_framework import status, serializers, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.authtoken.models import Token  # si token auth
from rest_framework.decorators import action

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import User, Couturiere, UserDocuments, Dropshipper 
from .serializers import (
    CustomTokenObtainPairSerializer,
    UserDocumentsSerializer,
    CouturiereSignupSerializer,
    ChangePasswordSerializer,
    ModelFilesSerializer,
)

from .utils import (
    send_verification_email,
    generate_otp,
    generate_signed_otp_token,
    verify_signed_otp_token,
)





User = get_user_model()

# User section

class Command(BaseCommand):
    help = 'Supprime les utilisateurs inactifs dont les tokens ont expiré.'

    def handle(self, *args, **kwargs):
        expired_users = User.objects.filter(is_active=False, token_expiration__lt=timezone.now())
        count = expired_users.count()
        expired_users.delete()
        self.stdout.write(self.style.SUCCESS(f"{count} utilisateurs supprimés."))


def verify_email(request, uid, token):
    try:
        # Décoder l'uid et récupérer l'utilisateur uniquement par ID
        user_id = urlsafe_base64_decode(uid).decode()
        user = User.objects.get(id=user_id)

        login_link = "http://localhost:5173/login"  # URL de ton frontend (change si besoin)

        # Si déjà activé
        if user.is_active:
            return HttpResponse(f'''
                <!DOCTYPE html>
                <html lang="ar" dir="rtl">
                    <head>
                    <meta charset="UTF-8">
                    <title>البريد الإلكتروني مفعل مسبقاً</title>
                    </head>
                    <body style="font-family: 'Cairo', sans-serif; background-color: #f4f4f4; text-align: center; padding: 50px;">
                    <div style="max-width: 600px; margin: auto; background-color: #ffffff; padding: 30px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                        <h2 style="color: #E5B62B;">تم تفعيل بريدك الإلكتروني بالفعل</h2>
                        <p style="font-size: 16px; color: #333;">يمكنك الآن تسجيل الدخول مباشرة إلى حسابك.</p>
                        <a href="{login_link}" style="display: inline-block; margin-top: 20px; padding: 12px 24px; background-color: #E5B62B; color: white; text-decoration: none; border-radius: 6px; font-size: 16px;">الانتقال إلى صفحة تسجيل الدخول</a>
                    </div>
                    </body>
                </html>
            ''')

        # Vérifier que le token est correct si le compte n'est pas activé
        if user.email_verification_token != token:
            return HttpResponse('Lien de vérification invalide ou expiré.', status=400)

        # Si token correct, activer le compte
        user.is_active = True
        user.email_verification_token = None  # Vider le token après vérification
        user.save()

        # Après succès :
        return HttpResponse(f'''
            <!DOCTYPE html>
            <html lang="ar" dir="rtl">
                <head>
                <meta charset="UTF-8">
                <title>تم التحقق من البريد الإلكتروني</title>
                </head>
                <body style="font-family: 'Cairo', sans-serif; background-color: #f4f4f4; text-align: center; padding: 50px;">
                <div style="max-width: 600px; margin: auto; background-color: #ffffff; padding: 30px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                    <h2 style="color: #E5B62B;">تم التحقق من بريدك الإلكتروني بنجاح</h2>
                    <p style="font-size: 16px; color: #333;">يمكنك الآن تسجيل الدخول إلى حسابك.</p>
                    <a href="{login_link}" style="display: inline-block; margin-top: 20px; padding: 12px 24px; background-color: #E5B62B; color: white; text-decoration: none; border-radius: 6px; font-size: 16px;">الانتقال إلى صفحة تسجيل الدخول</a>
                </div>
                </body>
            </html>
        ''')
    except (User.DoesNotExist, ValueError, TypeError):
        return HttpResponse('Lien de vérification invalide ou expiré.', status=400)

class ResendVerificationEmailView(APIView):
    def post(self, request):
        email = request.data.get("email")
        try:
            user = User.objects.get(email=email, is_active=False)
            user.generate_email_verification()
            user.save()
            send_verification_email(user)
            return Response({"message": "Email renvoyé."})
        except User.DoesNotExist:
            return Response({"error": "Utilisateur non trouvé ou déjà activé"}, status=404)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class ForgotPasswordView(APIView):
    def post(self, request):
        email = request.data.get("email")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"detail": "هذا البريد الإلكتروني غير مسجل."}, status=400)

        otp = generate_otp()
        signed_token = generate_signed_otp_token(email, otp)

        # Envoie du code OTP par email
        send_mail(
            subject="رمز إعادة تعيين كلمة المرور",
            message=f"رمز التحقق الخاص بك هو: {otp}",
            from_email="kadi@google.com",  
            recipient_list=[email],
        )

        return Response({
            "detail": "تم إرسال رمز التحقق إلى بريدك الإلكتروني.",
            "token": signed_token  # Tu l'envoies au frontend, ou le caches côté client (localStorage/sessionStorage)
        })

class VerifyOTPView(APIView):
    def post(self, request):
        token = request.data.get("token")
        otp = request.data.get("otp")

        if not all([token, otp]):
            return Response({"detail": "البيانات غير مكتملة."}, status=400)

        try:
            email = verify_signed_otp_token(token, otp)
        except serializers.ValidationError as e:
            return Response({"detail": e.detail[0]}, status=400)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"detail": "المستخدم غير موجود."}, status=404)

        final_reset_token = signing.dumps({"email": email}, salt="final-password-reset")

        return Response({
            "detail": "تم التحقق من الرمز بنجاح.",
            "reset_token": final_reset_token,
            "email": user.email 
        })

class ResetPasswordView(APIView):
    def post(self, request):
        reset_token = request.data.get("reset_token")
        new_password = request.data.get("new_password")

        if not all([reset_token, new_password]):
            return Response({"detail": "البيانات غير مكتملة."}, status=400)

        try:
            data = signing.loads(reset_token, salt="final-password-reset", max_age=600)
            email = data["email"]
        except signing.SignatureExpired:
            return Response({"detail": "انتهت صلاحية الرابط."}, status=400)
        except signing.BadSignature:
            return Response({"detail": "رمز غير صالح."}, status=400)

        try:
            user = User.objects.get(email=email)
            if not user.is_active:
                return Response({"detail": "الحساب غير مفعل."}, status=400)
        except User.DoesNotExist:
            return Response({"detail": "المستخدم غير موجود."}, status=404)

        user.set_password(new_password)
        user.save()

        # If you need to invalidate all existing tokens for this user
        try:
            refresh = RefreshToken.for_user(user)
            # If you have blacklist configured, uncomment:
            # refresh.blacklist()
        except Exception as e:
            print(f"Token handling error: {str(e)}")
            # Continue even if token handling fails

        return Response({"detail": "تم إعادة تعيين كلمة المرور بنجاح."})







# #couturiere section
# class CouturiereSignupView(APIView):
#     parser_classes = [MultiPartParser, FormParser]
    

#     def post(self, request):
#         serializer = CouturiereSignupSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             send_verification_email(user)
#             return Response(
#                 {"success": "Inscription réussie. Email de vérification envoyé."},
#                 status=status.HTTP_201_CREATED
#             )
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class CouturiereSignupView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        # COPY data and attach uploaded files list under 'documents'
        data = request.data.copy()
        files = request.FILES.getlist('documents') or request.FILES.getlist('files') or request.FILES.getlist('documents[]')
        if files:
            data.setlist('documents', files)

        serializer = CouturiereSignupSerializer(data=data, context={"request": request})
        if serializer.is_valid():
            user = serializer.save()
            send_verification_email(user)
            return Response({"success": "Inscription réussie. Email de vérification envoyé."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class UserDocumentsViewSet(viewsets.ModelViewSet):
#     queryset = UserDocuments.objects.all()
#     serializer_class = UserDocumentsSerializer


# class CouturiereViewSet(viewsets.ModelViewSet):
#     queryset = Couturiere.objects.all()
#     serializer_class = CouturiereSerializer

# @action(detail=True, methods=['post'])
# def upload_document(self, request, pk=None):
#     couturiere = self.get_object()
#     user = couturiere.user
#     documents = request.FILES.getlist('documents')

#     if not documents:
#         return Response({'error': 'Aucun fichier fourni'}, status=400)

#     if len(documents) > 5:
#         return Response({'error': 'Maximum 5 fichiers autorisés'}, status=400)

#     created_docs = []
#     for document in documents:
#         user_doc = UserDocuments(user=user, nom=document)
#         user_doc.save()  # La méthode save() gère les deux étapes
        
#         created_docs.append({
#             'id': user_doc.id,
#             'nom': user_doc.nom.name,
#             'user_id': user.id
#         })

#     return Response(created_docs, status=201)


# class DropshipperViewSet(viewsets.ModelViewSet):
#     queryset = Dropshipper.objects.all()
#     serializer_class = DropshipperSerializer

#     @action(detail=True, methods=['post'])
#     def upload_document(self, request, pk=None):
#         dropshipper = self.get_object()
#         user = dropshipper.user
#         documents = request.FILES.getlist('documents')

#         if not documents:
#             return Response({'error': 'Aucun fichier fourni'}, status=400)

#         if len(documents) > 5:
#             return Response({'error': 'Maximum 5 fichiers autorisés'}, status=400)

#         created_docs = []
#         for document in documents:
#             doc = UserDocuments.objects.create(
#                 nom=document,
#                 user=user
#             )
#             created_docs.append({
#                 'id': doc.id,
#                 'nom': doc.nom.name,
#                 'user_id': user.id
#             })

#         return Response(created_docs, status=201)










@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        # Récupérer l'utilisateur connecté
        user = request.user
        
        # Changer le mot de passe
        user.set_password(serializer.validated_data['newPassword'])
        user.save()
        
        return Response(
            {"message": "Mot de passe changé avec succès."},
            status=status.HTTP_200_OK
        )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    

User = get_user_model()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_client_name(request):
    """
    Retourne le nom du client authentifié
    """
    try:
        # Récupérer l'utilisateur connecté
        user = request.user
        
        # Retourner le nom du client
        return Response({
            'full_name': user.full_name,
            'email': user.email,
            'role': user.role
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': 'Erreur serveur'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        
        
        
        


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import FashionModel
from .serializers import CouturiereModelSerializer

class AddModelView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        # Vérifier qu'il y a au moins un fichier
        if not request.FILES.getlist("files"):
            return Response(
                {"error": "Vous devez inclure au moins un fichier."},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = CouturiereModelSerializer(data=request.data, context={"request": request})


        if serializer.is_valid():
            serializer.save()  # sécuriser encore une fois
    
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import FashionModel
from .serializers import FashionModelListSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import FashionModel
from .serializers import FashionModelListSerializer
class CouturiereModelsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.role != 'couturiere':
            return Response(
                {"error": "Accès réservé aux couturières"}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        models = FashionModel.objects.filter(owner=user)\
                                    .prefetch_related('images', 'variants')\
                                    .order_by("-created_at")
    
        serializer = FashionModelListSerializer(
            models,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


from .models import CustomOrder 
from .serializers import CustomOrderSerializer


class OffresFassouCouturiereModelsView(APIView):
    """
    Toutes les demandes fassou NON encore affectées à une couturière
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.role != "couturiere":
            return Response({"error": "Accès réservé aux couturières"}, status=status.HTTP_403_FORBIDDEN)

        demandes = CustomOrder.objects.filter(command_type="fassou", assigned_couturiere__isnull=True)
        serializer = CustomOrderSerializer(demandes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DemandesFassouCouturiereModelsView(APIView):
    """
    Toutes les offres fassou affectées à la couturière connectée
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.role != "couturiere":
            return Response({"error": "Accès réservé aux couturières"}, status=status.HTTP_403_FORBIDDEN)

        offres = CustomOrder.objects.filter(command_type="fassou", assigned_couturiere=user)
        serializer = CustomOrderSerializer(offres, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DemandesPersonaliseView(APIView):
    """
    Toutes les demandes personalise affectées à la couturière connectée
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.role != "couturiere":
            return Response({"error": "Accès réservé aux couturières"}, status=status.HTTP_403_FORBIDDEN)

        offres = CustomOrder.objects.filter(command_type="personalized", assigned_couturiere=user)
        serializer = CustomOrderSerializer(offres, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)






class ModifyFassouOfferView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        try:
            order = CustomOrder.objects.get(pk=pk, command_type="fassou")
        except CustomOrder.DoesNotExist:
            return Response({"error": "Offer not found"}, status=status.HTTP_404_NOT_FOUND)

        # Only couturiere can take the offer
        if request.user.role != "couturiere":
            return Response({"error": "Only couturiere can take offers"}, status=status.HTTP_403_FORBIDDEN)

        # Check if already assigned
        if order.assigned_couturiere is not None:
            return Response({"error": "This offer has already been taken"}, status=status.HTTP_400_BAD_REQUEST)

        # Update order
        order.state = "inprogress"
        order.assigned_couturiere = request.user
        order.save()

        serializer = CustomOrderSerializer(order, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)





from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from .models import Couturiere
from .serializers import UserAccountSerializer, CouturiereAccountSerializer,ChangePasswordWithVerificationSerializer,AffiliateAccountSerializer

User = get_user_model()

class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserAccountSerializer 
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class AffiliateProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = AffiliateAccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user 




class CouturiereProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = CouturiereAccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return Couturiere.objects.get(user=self.request.user)






@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password_with_verification(request):
    serializer = ChangePasswordWithVerificationSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        user = request.user
        
        # Vérifier l'ancien mot de passe
        if not user.check_password(serializer.validated_data['current_password']):
            return Response({"current_password": "Mot de passe actuel incorrect."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Changer le mot de passe
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        return Response(
            {"message": "Mot de passe changé avec succès."},
            status=status.HTTP_200_OK
        )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)












from rest_framework import generics, permissions
from .models import PromoCode
from .serializers import PromoCodeSerializer

class AffiliatePromoCodeListView(generics.ListAPIView):
    serializer_class = PromoCodeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only promo codes for the logged-in affiliate
        return PromoCode.objects.filter(affiliate=self.request.user)











# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Count
from .models import Order
from .serializers import AffiliateOrderSerializer
# views.py
class AffiliateOrdersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        affiliate = request.user
        orders = (
            Order.objects.filter(
                state="done",
                promo_code__affiliate=affiliate
            )
            .select_related("promo_code", "fashion_model")
            .prefetch_related("standard_command_details")
        )

        serializer = AffiliateOrderSerializer(orders, many=True)

        # Totals
        total_orders = orders.count()

        total_discounts = 0
        total_profit = 0

        for o in orders:
            quantity = sum(v.quantity for v in o.standard_command_details.all())
            base_price = o.fashion_model.price_per_piece_for_client * quantity

            discount = 0
            if o.promo_code:
                discount = base_price * (o.promo_code.discount_percentage / 100)
                profit = (base_price - discount) * (o.promo_code.profit_percentage / 100)
                total_profit += profit

            total_discounts += discount

        return Response({
            "orders": serializer.data,
            "totals": {
                "total_orders": total_orders,
                "total_discounts": total_discounts,
                "total_profit": total_profit
            }
        })
