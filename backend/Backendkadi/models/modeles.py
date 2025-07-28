from django.db import models
from .stock import StockVariant
from .promo import PromoCode

TYPE_CHOICES = [
    ('dress', 'Robe'),
    ('abaya', 'Abaya'),
    ('ensemble', 'Ensemble'),
]

class FashionModel(models.Model):
    STATE_CHOICES = [
        ('accepted', 'Accepted'),
        ('waiting', 'Waiting'),
        ('cancelled', 'Cancelled'),
    ]

    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    
    price_per_piece_for_client = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_piece_for_dropshipper = models.DecimalField(max_digits=10, decimal_places=2)
    
    description = models.TextField()
    folder = models.ImageField(upload_to='models/', blank=True, null=True)
    min_pieces_for_dropshipper = models.PositiveIntegerField()

    variants = models.ManyToManyField(StockVariant, related_name='fashion_models')
    
    state = models.CharField(max_length=20, choices=STATE_CHOICES, default='waiting')
    promo_code = models.ForeignKey(PromoCode, on_delete=models.SET_NULL, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def total_pieces(self):
        return sum(variant.quantity for variant in self.variants.all())

    def available_quantity(self):
        return sum(v.quantity for v in self.variants.all() if v.quantity > 0)

    def __str__(self):
        return f"{self.name} ({self.code})"
