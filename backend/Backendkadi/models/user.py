from django.db import models
from datetime import timedelta
from django.contrib.auth.models import AbstractUser
import secrets, string
from django.utils import timezone

class User(AbstractUser):
    ROLE_CHOICES = [
        ('couturiere', 'Couturière'),
        ('dropshipper', 'Dropshipper'),
        ('affiliate', 'Affilié'),
        ('client', 'Client'),
    ]

    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #ajouter dans  la premiere signup verification de l'email
    email_verification_token = models.CharField(max_length=64, null=True, blank=True)
    token_expiration = models.DateTimeField(null=True, blank=True)
    # Supprimer les champs par défaut qu’on n’utilise pas
    username = None
    first_name = None
    last_name = None
    is_active = models.BooleanField(default=False)

    # Auth basé sur l’email
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'role']  # Ce que Django demandera à `createsuperuser`

    def generate_email_verification(self):
        chars = string.ascii_letters + string.digits
        self.email_verification_token = ''.join(secrets.choice(chars) for _ in range(32))
        self.token_expiration = timezone.now() + timedelta(hours=24)
            
    def __str__(self):
        return self.full_name

class Couturiere(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField()
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    is_accepted = models.BooleanField(default=False)
    agreed_to_policy = models.BooleanField(default=False)

class Dropshipper(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    store_link = models.TextField()
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    is_accepted = models.BooleanField(default=False)
    agreed_to_policy = models.BooleanField(default=False)

class Client (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    agreed_to_policy = models.BooleanField(default=False)

    def __str__(self):
        return f"Affiliate: {self.user.full_name}"


# class Affiliate(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)

#     def __str__(self):
#         return f"Affiliate: {self.user.full_name}"


# import secrets
# import os

# def custom_upload_path(instance, filename):
#     """Génère un chemin unique : user_type/userID/randomID_filename"""
#     user_type = 'couturiere' if instance.couturiere else 'dropshipper'
#     user_id = instance.couturiere.id if instance.couturiere else instance.dropshipper.id
#     random_id = secrets.token_hex(4)
#     base, ext = os.path.splitext(filename)
#     return f'user_docs/{user_type}_{user_id}/{random_id}_{base}{ext}'

# class UserDocuments(models.Model):
#     nom = models.FileField(upload_to=custom_upload_path)
#     couturiere = models.ForeignKey(
#         'Couturiere', 
#         on_delete=models.CASCADE, 
#         null=True, 
#         blank=True,
#         related_name='documents'
#     )
#     dropshipper = models.ForeignKey(
#         'Dropshipper',
#         on_delete=models.CASCADE,
#         null=True,
#         blank=True,
#         related_name='documents'
#     )
#     uploaded_at = models.DateTimeField(default=timezone.now)

#     class Meta:
#         verbose_name_plural = "User Documents"

#     def __str__(self):
#         return f"Document #{self.id}"
import os
from django.db import models
from django.utils import timezone


# def custom_upload_path(instance, filename):
#     """
#     Stocke dans : user_docs/<role>/<nom>_<id>.ext
#     Exemple : user_docs/couturiere/facture_1.pdf
#     """
#     # On récupère le rôle depuis l'utilisateur
#     role = instance.user.role  # 'couturiere' ou 'dropshipper'
#     base, ext = os.path.splitext(filename)

#     # Si pas encore d'ID → fichier temporaire
#     doc_id = instance.id if instance.id else 'temp'

#     return f"user_docs/{role}/{base}_{doc_id}{ext}"


# class UserDocuments(models.Model):
#     nom = models.FileField(upload_to=custom_upload_path)
#     user = models.ForeignKey(
#         'User',  # ton modèle User personnalisé
#         on_delete=models.CASCADE,
#         null=True,  # Ajoutez ceci temporairement
#         blank=True,  # Ajoutez ceci temporairement
#         related_name='documents'
#     )
#     uploaded_at = models.DateTimeField(default=timezone.now)

#     class Meta:
#         verbose_name_plural = "User Documents"

#     def save(self, *args, **kwargs):
#         # Si pas encore d'ID → on sauvegarde une 1ère fois pour l'obtenir
#         if not self.id:
#             temp_file = self.nom
#             self.nom = None
#             super().save(*args, **kwargs)
#             self.nom = temp_file
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"Document #{self.id}"


def custom_upload_path(instance, filename):
    """
    Génère le chemin final après que l'instance a un ID
    Format: user_docs/<role>/<nom_base>_<id>.<ext>
    """
    if not instance.id:
        return 'temp_uploads/temp_file'  # Chemin temporaire pour la première sauvegarde
    
    role = instance.user.role
    base, ext = os.path.splitext(filename)
    return f'user_docs/{role}/{base}_{instance.id}{ext}'
class UserDocuments(models.Model):
    nom = models.FileField(upload_to=custom_upload_path)
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='documents',
        null=True,
        blank=True,
    )
    uploaded_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "User Documents"

    def save(self, *args, **kwargs):
        # Sauvegarde en deux étapes pour avoir l'ID avant le nom final
        if not self.id:
            # Première sauvegarde pour obtenir un ID
            temp_file = self.nom
            self.nom = None
            super().save(*args, **kwargs)
            self.nom = temp_file
            kwargs.pop('force_insert', None)  # Important pour éviter les doublons
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Document #{self.id}"
    
    
    