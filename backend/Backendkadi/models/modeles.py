from django.db import models
from .promo import PromoCode
from django.contrib.auth import get_user_model
import uuid

# Get the user model at the module level
User = get_user_model()
TYPE_CHOICES = [
    ('femme', 'Femme'),
    ('homme', 'Homme'),
    ('enfant', 'Enfant'),
    ('babie','Babie'),
] 

import string
from django.db import models

def encode_base36(num):
    chars = string.digits + string.ascii_uppercase  # 0-9 + A-Z
    base = len(chars)
    result = ""
    while num > 0:
        num, rem = divmod(num, base)
        result = chars[rem] + result
    return result or "0"
class FashionModel(models.Model):
    STATE_CHOICES = [
        ('accepted', 'Accepted'),
        ('waiting', 'Waiting'),
        ('cancelled', 'Cancelled'),
    ]



    name = models.CharField(max_length=255)
    code = models.CharField(
        max_length=10,
        unique=True, 
        blank=True,          # on laisse vide pour le générer après
        editable=False
    )    
    
    
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    price=models.DecimalField(max_digits=20,decimal_places=2,default=0)
    price_per_piece_for_client = models.DecimalField(max_digits=20, decimal_places=2,blank=False,null=False)
    price_per_piece_for_dropshipper = models.DecimalField(max_digits=20, decimal_places=2,default=0)
    
    description = models.TextField()
    min_pieces_for_dropshipper = models.PositiveIntegerField(default=1)



    state = models.CharField(max_length=20, choices=STATE_CHOICES, default='waiting')
    promo_codes = models.ManyToManyField(PromoCode, blank=True, related_name='models_CodePromo')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    owner = models.ForeignKey(         
        User,
        on_delete=models.CASCADE,
        related_name='fashion_models',
        limit_choices_to={'role': 'couturiere'},
    )
    
    def save(self, *args, **kwargs):
        # Sauvegarder une première fois pour générer l'ID
        if not self.id:
            super().save(*args, **kwargs)
        # Si le code n’existe pas encore → générer à partir de l’ID
        if not self.code:
            self.code = encode_base36(self.id).zfill(4)  # min 4 caractères
            return super().save(update_fields=["code"])
        return super().save(*args, **kwargs)



    def total_pieces(self):
        return sum(variant.quantity for variant in self.variants.all())

    def available_quantity(self):
        return sum(v.quantity for v in self.variants.all() if v.quantity > 0)

    def __str__(self):
        return f"{self.name} ({self.code})"




class ModelImage(models.Model):
    fashion_model = models.ForeignKey(
        FashionModel, 
        on_delete=models.CASCADE, 
        related_name='images'
    )
    image = models.FileField(upload_to='models/')

    def __str__(self):
        return f"Image for {self.fashion_model.code}"
