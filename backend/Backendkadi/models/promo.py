# models/promotions.py (ou dans commandes.py si tu n’as pas beaucoup de fichiers)

from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()
class PromoCode(models.Model):
    code = models.CharField(max_length=20, unique=True)

    affiliate = models.ForeignKey(
        User, on_delete=models.CASCADE, limit_choices_to={'role': 'affiliate'},    null=True,
    blank=True,
    related_name='promo_codes'
    )

    # Combien l’affilié gagne
    profit_percentage = models.DecimalField(max_digits=5, decimal_places=2)  # ex: 10.0 = 10%

    # Réduction appliquée au client
    discount_percentage = models.DecimalField(
        max_digits=5, decimal_places=2, help_text="Réduction visible par le client"
    )

    start_date = models.DateField()
    expiration_date = models.DateField()


    usage_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def is_valid(self):
    #     from datetime import date
    #     today = date.today()
    #     return self.state == 'active' and self.start_date <= today <= self.expiration_date

    def __str__(self):
        return self.code

