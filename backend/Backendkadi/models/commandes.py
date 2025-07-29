from django.db import models
from django.contrib.auth import get_user_model
from .stock import StockVariant
from .modeles import TYPE_CHOICES ,FashionModel
from .promo import PromoCode  # adapte le chemin si besoin

User = get_user_model()

STATE_CHOICES = [
    ('pending', 'En cours'),
    ('done', 'Terminé'),
    ('cancelled', 'Annulé'),
]
class CustomOrder(models.Model):
    COMMAND_TYPE_CHOICES = [
        ('fassou', 'Fassou'),
        ('personalized', 'Personnalisée'),
    ]


    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'client'},
        related_name='custom_orders'
    )

    command_type = models.CharField(max_length=20, choices=COMMAND_TYPE_CHOICES)
    model_type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    initial_price = models.DecimalField(max_digits=10, decimal_places=2)
    deadline = models.DateField()
    description = models.TextField(blank=True, null=True)

    command_details = models.ManyToManyField(StockVariant, related_name='orders')
    
    promo_code = models.ForeignKey(PromoCode, on_delete=models.SET_NULL, null=True, blank=True, related_name='commandes')

    image_folder = models.FileField(upload_to='custom_orders/', blank=True, null=True)
    state = models.CharField(max_length=20, choices=STATE_CHOICES, default='pending')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def total_requested_quantity(self):
        return sum(variant.quantity for variant in self.command_details.all())

    def __str__(self):
        return f"{self.command_type.capitalize()} de {self.user.full_name} ({self.created_at.date()})"




# this is for the  simple standard order for the client and the dropshipper
class Order(models.Model):


    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': {'client','dropshipper'}},
        related_name='standard_orders',
        null=True,
        blank=True
    )

    phone_number = models.CharField(max_length=20)
    address = models.TextField()

    fashion_model = models.ForeignKey(
        FashionModel,
        on_delete=models.CASCADE,
        related_name='orders'
    )

    standard_command_details = models.ManyToManyField(StockVariant, related_name='orders_standard')

    initial_price = models.DecimalField(max_digits=10, decimal_places=2)
    promo_code = models.ForeignKey(PromoCode, on_delete=models.SET_NULL, null=True, blank=True, related_name='standard_orders')

    delivery_price = models.DecimalField(max_digits=10, decimal_places=2)

    state = models.CharField(max_length=20, choices=STATE_CHOICES, default='pending')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def final_price(self):
        discount = (self.promo_code.discount_percent / 100) if self.promo_code else 0
        return round((self.initial_price * (1 - discount)) + self.delivery_price, 2)

    def __str__(self):
        return f"Commande {self.id} de {self.user.full_name} ({self.created_at.date()})"


