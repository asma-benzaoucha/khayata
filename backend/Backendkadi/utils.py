from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings
from django.core import signing
import random
from django.core.mail import EmailMultiAlternatives
from rest_framework import serializers

def send_verification_email(user_or_couturiere):
    user = getattr(user_or_couturiere, 'user', user_or_couturiere)
    if not hasattr(user, 'email_verification_token'):
        raise AttributeError("L'utilisateur n'a pas de champ 'email_verification_token'")

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = user.email_verification_token
    verification_link = f"http://localhost:8000/api/verify-email/{uid}/{token}"
    login_link = "http://localhost:5173/login"  # Change l'URL selon ton frontend

    subject = 'تأكيد بريدك الإلكتروني - Kadi'
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [user.email]

    # Texte brut (fallback)
    text_content = f"""مرحباً {user.full_name},
يرجى تأكيد بريدك الإلكتروني بالنقر على الرابط التالي:
{verification_link}
شكراً لك!
"""

    # HTML INLINE
    html_content = f"""
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
      <head>
        <meta charset="UTF-8" />
        <title>تأكيد بريدك الإلكتروني</title>
      </head>
      <body style="font-family: 'Arial', sans-serif; background-color: #f9f9f9; padding: 20px;">
        <div style="max-width: 600px; margin: auto; background-color: #ffffff; padding: 20px; border-radius: 10px; text-align: center;">
          <img src="https://your-domain.com/static/logo.png" alt="Kadi Logo" style="width: 120px; margin-bottom: 20px;" />
          <h2 style="color: #E5B62B;">مرحباً {user.full_name}</h2>
          <p style="font-size: 16px; color: #333;">. "يرجى تأكيد بريدك الإلكتروني لإكمال عملية التسجيل في "قاضي للأزياء و الاستثمار    </p>
          <a href="{verification_link}" style="display: inline-block; margin-top: 20px; padding: 12px 24px; background-color: #E5B62B; color: white; text-decoration: none; border-radius: 6px; font-size: 16px;">تأكيد البريد الإلكتروني</a>
          <p style="font-size: 14px; color: #777; margin-top: 30px;">بعد التحقق، يمكنك تسجيل الدخول من هنا:</p>
          <a href="{login_link}" style="font-size: 14px; color: #4A66BD;">صفحة تسجيل الدخول</a>
        </div>
      </body>
    </html>
    """

    msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    msg.attach_alternative(html_content, "text/html")
    msg.send()






def generate_otp():
    return f"{random.randint(100000, 999999)}"

def generate_signed_otp_token(email, otp):
    payload = {
        "email": email,
        "otp": otp
    }
    return signing.dumps(payload, salt="password-reset-code")


def verify_signed_otp_token(token, otp, max_age=600):
    try:
        data = signing.loads(token, salt="password-reset-code", max_age=max_age)
        if data["otp"] != otp:
            raise serializers.ValidationError("رمز التحقق غير صحيح.")
        return data["email"]
    except signing.SignatureExpired:
        raise serializers.ValidationError("انتهت صلاحية رمز التحقق.")
    except signing.BadSignature:
        raise serializers.ValidationError("رمز التحقق غير صالح.")

