from django.db import models
from webcolors import CSS3_NAMES_TO_HEX
from .modeles import FashionModel


class BaseVariant(models.Model):
    SIZE_CHOICES = [
        ('XS', 'XS'), ('S', 'S'), ('M', 'M'),
        ('L', 'L'), ('XL', 'XL'), ('XXL', 'XXL'), ('XXXL', 'XXXL'),
        ('3XL', '3XL'), ('4XL', '4XL'),
    ]
    
    COLOR_CHOICES = [(name, name) for name in CSS3_NAMES_TO_HEX]

    size = models.CharField(choices=SIZE_CHOICES, null=True)
    color = models.CharField(max_length=20, choices=COLOR_CHOICES, null=True)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        abstract = True



class StockVariantForCommands(BaseVariant):
    def str(self):
        return f"[Command] {self.color} - {self.size} ({self.quantity})"


class StockVariantForFashionModels(BaseVariant):
    fashion_model = models.ForeignKey(
        FashionModel,
        on_delete=models.CASCADE,
        related_name="variants",
        null=False,
        blank=False
    )

    def str(self):
        if self.fashion_model:
            return f"[Model {self.fashion_model.code}] {self.color} - {self.size} ({self.quantity})"
        return f"[Model] Unassigned - {self.color} - {self.size} ({self.quantity})"