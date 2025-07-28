from django.db import models
from webcolors import CSS3_NAMES_TO_HEX

class StockVariant(models.Model):
    SIZE_CHOICES = [
        ('XS', 'XS'), ('S', 'S'), ('M', 'M'),
        ('L', 'L'), ('XL', 'XL'), ('XXL', 'XXL'), ('XXXL', 'XXXL'),
        ('3XL', '3XL'), ('4XL', '4XL'),
        ('0–3 mois', '0–3 mois'), ('6–12 mois', '6–12 mois'),
    ]
    COLOR_CHOICES = [(name, name) for name in CSS3_NAMES_TO_HEX]

    size = models.CharField(choices=SIZE_CHOICES, null=True)
    color = models.CharField(max_length=20, choices=COLOR_CHOICES, null=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        related_model = self.fashion_models.first()
        if related_model:
            return f"{related_model.code} - {self.size} - {self.color} ({self.quantity})"
        return f"Unassigned variant - {self.size} - {self.color} ({self.quantity})"
