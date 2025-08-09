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

from .models import User, Couturiere, UserDocuments, Dropshipper
from .serializers import (
    CouturiereSerializer,
    CustomTokenObtainPairSerializer,
    LoginSerializer,
    UserDocumentsSerializer,
    CouturiereSignupSerializer,
)
from .utils import (
    send_verification_email,
    generate_otp,
    generate_signed_otp_token,
    verify_signed_otp_token,
)

class Command(BaseCommand):
    help = 'Supprime les utilisateurs inactifs dont les tokens ont expiré.'

    def handle(self, *args, **kwargs):
        expired_users = User.objects.filter(is_active=False, token_expiration__lt=timezone.now())
        count = expired_users.count()
        expired_users.delete()
        self.stdout.write(self.style.SUCCESS(f"{count} utilisateurs supprimés."))

User = get_user_model()

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

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']

            # Générer ou récupérer un token
            token, created = Token.objects.get_or_create(user=user)

            return Response({
                'token': token.key,
                'user_id': user.id,
                'email': user.email,
                'full_name': user.full_name,
                'role': user.role
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

User = get_user_model()
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

User = get_user_model()
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


class CouturiereSignupView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = CouturiereSignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            send_verification_email(user)
            return Response(
                {"success": "Inscription réussie. Email de vérification envoyé."},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDocumentsViewSet(viewsets.ModelViewSet):
    queryset = UserDocuments.objects.all()
    serializer_class = UserDocumentsSerializer


class CouturiereViewSet(viewsets.ModelViewSet):
    queryset = Couturiere.objects.all()
    serializer_class = CouturiereSerializer

@action(detail=True, methods=['post'])
def upload_document(self, request, pk=None):
    couturiere = self.get_object()
    user = couturiere.user
    documents = request.FILES.getlist('documents')

    if not documents:
        return Response({'error': 'Aucun fichier fourni'}, status=400)

    if len(documents) > 5:
        return Response({'error': 'Maximum 5 fichiers autorisés'}, status=400)

    created_docs = []
    for document in documents:
        user_doc = UserDocuments(user=user, nom=document)
        user_doc.save()  # La méthode save() gère les deux étapes
        
        created_docs.append({
            'id': user_doc.id,
            'nom': user_doc.nom.name,
            'user_id': user.id
        })

    return Response(created_docs, status=201)


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