from django.db import models
from .promo import PromoCode
from django.contrib.auth import get_user_model
import uuid
import string
from django.db import models
User = get_user_model()
TYPE_CHOICES = [
    ('femme', 'femme'),
    ('homme', 'homme'),
    ('enfant', 'enfant'), 
] 

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
        ('notvisible','nonvisible')
    ]
    owner = models.ForeignKey(         
        User,
        on_delete=models.CASCADE,
        related_name='submitted_models',
        limit_choices_to={'role': 'couturiere'},
        null=True,  # Ajoutez ceci
        blank=True, 
    )
    name = models.CharField(max_length=255)
    code = models.CharField(
        max_length=50, 
        unique=True, 
        blank=True,
        editable=False
    )
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    
    price_per_piece_for_client = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    price_per_piece_for_dropshipper = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    
    description = models.TextField()
    min_pieces_for_dropshipper = models.PositiveIntegerField(default=1)

    # variants = models.ManyToManyField(StockVariant, related_name='fashion_models')
    # #totalquantity=models.PositiveIntegerField(default=100000)
    state = models.CharField(max_length=20, choices=STATE_CHOICES, default='waiting')
    promo_code = models.ForeignKey(PromoCode, on_delete=models.SET_NULL, blank=True, null=True, related_name='models')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    
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
    image = models.ImageField(upload_to='models/')

    def __str__(self):
        return f"Image for {self.fashion_model.code}"