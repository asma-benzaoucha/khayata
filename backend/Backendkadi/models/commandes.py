from django.db import models
from django.contrib.auth import get_user_model
from .stock import StockVariant
from .modeles import TYPE_CHOICES ,FashionModel
from .promo import PromoCode  # adapte le chemin si besoin
from django.core.validators import RegexValidator

User = get_user_model()

STATE_CHOICES = [
    ('pending', 'En cours'),#pending c'est la valeur stoqué dans bdd et en cours libellé utilisateur
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
    nameorder=models.CharField(max_length=50, blank=False, null=False)
    numTelephone = models.CharField(max_length=10,validators=[RegexValidator(r'^\d{10}$', 'Le numéro doit contenir exactement 10 chiffres.')],blank=False, null=False)
    exactaddress=models.CharField(max_length=50,blank=False, null=False)
    wilaya = models.ForeignKey( "WilayaDelivery", on_delete=models.CASCADE, related_name="customorders_details",null=False, blank=False,)
    initial_price= models.DecimalField(max_digits=10, decimal_places=2, blank=True,null=True)
    command_type = models.CharField(max_length=20, choices=COMMAND_TYPE_CHOICES)
    model_type = models.CharField(max_length=20, choices=TYPE_CHOICES, null=True)
    deadline = models.DateField()
    description = models.TextField(blank=True, null=True)
    command_details = models.ManyToManyField(StockVariant, related_name='orders')
    state = models.CharField(max_length=20, choices=STATE_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def total_requested_quantity(self):
        return sum(variant.quantity for variant in self.command_details.all())

    def __str__(self):
        return f"{self.command_type.capitalize()} de {self.user.full_name} ({self.created_at.date()})"



class CustomOrderImage(models.Model):
    fashion_model = models.ForeignKey(
        CustomOrder, 
        on_delete=models.CASCADE, 
        related_name='custom_images'
    )
    image = models.ImageField(upload_to='mycustomorders/')



# this is for the  simple standard order for the client and the dropshipper
class Order(models.Model):


    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role__in': ['client', 'dropshipper']},
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
    promo_code = models.ForeignKey(PromoCode, on_delete=models.SET_NULL, null=True, blank=True, related_name='standard_orders')

    wilaya = models.ForeignKey(
        "WilayaDelivery", 
        on_delete=models.CASCADE, 
        related_name="orders",
        null=True,
        blank=True,
    )

    state = models.CharField(max_length=20, choices=STATE_CHOICES, default='pending')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def final_price(self):
        discount = (self.promo_code.discount_percent / 100) if self.promo_code else 0
        return round((self.initial_price * (1 - discount)) + self.delivery_price, 2)

    def __str__(self):
        return f"Commande {self.id} de {self.user.full_name} ({self.created_at.date()})"


