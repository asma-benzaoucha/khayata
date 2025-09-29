from django.db import models
from datetime import timedelta
from django.contrib.auth.models import AbstractUser
import secrets, string
from django.utils import timezone
import os
from .managers import CustomUserManager
from .livraison import  WilayaDelivery

class User(AbstractUser):
    ROLE_CHOICES = [
        ('couturiere', 'Couturière'),
        ('dropshipper', 'Dropshipper'),
        ('affiliate', 'Affilié'),
        ('client', 'Client'),
        ('admin', 'Administrateur'),
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
    objects = CustomUserManager()

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
    
    
class Client (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    agreed_to_policy = models.BooleanField(default=False)

    def __str__(self):
        return f"Client: {self.user.full_name}"

class Affiliate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=10, blank=True, null=True)
    
    
class Couturiere(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField()
    phone_number = models.CharField(max_length=10, blank=False, null=False)  
    is_accepted = models.BooleanField(null=True,blank=True)
    agreed_to_policy = models.BooleanField(default=False)
    refused_at = models.DateTimeField(null=True, blank=True)


class Dropshipper(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    store_link = models.TextField()
    phone_number = models.CharField(max_length=10, blank=False, null=False)# 
    is_accepted = models.BooleanField(blank=True, null=True)
    agreed_to_policy = models.BooleanField(default=False)
    refused_at = models.DateTimeField(null=True, blank=True)


class DropshipperClients(models.Model):
    dropshipper = models.ForeignKey(
        'Dropshipper', 
        on_delete=models.CASCADE,
        related_name='clients'
    )
    nom_client = models.CharField(max_length=100, blank=False, null=False)
  
    
    class Meta:
        verbose_name = "Client Dropshipper"
        verbose_name_plural = "Clients Dropshippers"
       
    
    def __str__(self):
        return f"{self.nom_client}"



import os, uuid
from django.utils import timezone
from django.db import models
def custom_upload_path(instance, filename):
    role = instance.user.role if instance.user else "unknown"
    base, ext = os.path.splitext(filename)
    unique = uuid.uuid4().hex[:8]
    return f"user_docs/{role}/{base}_{unique}{ext}"

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

    def __str__(self):
        return f"Document #{self.id}"
    
    
    