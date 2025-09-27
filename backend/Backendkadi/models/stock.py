# from django.db import models
# from webcolors import CSS3_NAMES_TO_HEX
# from .modeles import FashionModel

# class StockVariantForCommands(models.Model):
#     SIZE_CHOICES = [
#         ('XS', 'xs'), ('S', 's'), ('M', 'm'),
#         ('L', 'l'), ('XL', 'xl'), ('XXL', 'XXL'), ('XXXL', 'XXXL'),
#         ('3XL', '3XL'), ('4XL', '4XL'),
#     ]
#     COLOR_CHOICES = [(name, name) for name in CSS3_NAMES_TO_HEX]    
    
#     size = models.CharField(choices=SIZE_CHOICES, null=True)
#     color = models.CharField(max_length=20, choices=COLOR_CHOICES, null=True)
#     quantity = models.PositiveIntegerField(default=1)

#     def __str__(self):
#         return f"{self.color} - {self.size} ({self.quantity})"





# class StockVariantForFashionModels(models.Model):
#     SIZE_CHOICES = [
#         ('XS', 'XS'), ('S', 'S'), ('M', 'M'),
#         ('L', 'L'), ('XL', 'XL'), ('XXL', 'XXL'), ('XXXL', 'XXXL'),
#         ('3XL', '3XL'), ('4XL', '4XL'),
#     ]
#     COLOR_CHOICES = [(name, name) for name in CSS3_NAMES_TO_HEX]
#     fashion_model = models.ForeignKey(
#         FashionModel, 
#         on_delete=models.CASCADE, 
#         related_name='variants',
#         null=True,  
#         blank=True
#     )
#     size = models.CharField(choices=SIZE_CHOICES, null=True)
#     color = models.CharField(max_length=20, choices=COLOR_CHOICES, null=True)
#     quantity = models.PositiveIntegerField(default=1)

#     def str(self):
#         related_model = self.fashion_models.first()
#         if related_model:
#             return f"{related_model.code} - {self.size} - {self.color} ({self.quantity})"
#         return f"Unassigned variant - {self.size} - {self.color} ({self.quantity})"

















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
    def __str__(self):
        return f"[Command] {self.color} - {self.size} ({self.quantity})"



class StockVariantForFashionModels(BaseVariant):
    fashion_model = models.ForeignKey(
        FashionModel,
        on_delete=models.CASCADE,
        related_name="variants",
        null=False,
        blank=False
    )

    def __str__(self):
        if self.fashion_model:
            return f"[Model {self.fashion_model.code}] {self.color} - {self.size} ({self.quantity})"
        return f"[Model] Unassigned - {self.color} - {self.size} ({self.quantity})"

