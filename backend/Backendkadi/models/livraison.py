from django.db import models

class WilayaDelivery(models.Model):
    wilaya_name = models.CharField(max_length=100, unique=True)
    delivery_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.wilaya_name} - {self.delivery_price} DA"
