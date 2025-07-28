from django.db import models

class User(models.Model):
    ROLE_CHOICES = [
        ('couturiere', 'Couturière'),
        ('dropshipper', 'Dropshipper'),
        ('affiliate', 'Affilié'),
        ('client', 'Client'),
    ]

    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name

class Couturiere(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField()
    folder = models.FileField(upload_to='dossiers/', blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    is_accepted = models.BooleanField(default=False)
    agreed_to_policy = models.BooleanField(default=False)



class Dropshipper(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    store_link = models.TextField()
    folder = models.FileField(upload_to='dossiers/', blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    is_accepted = models.BooleanField(default=False)
    agreed_to_policy = models.BooleanField(default=False)

class Client (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    agreed_to_policy = models.BooleanField(default=False)

    def __str__(self):
        return f"Affiliate: {self.user.full_name}"

    
# class Affiliate(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)

#     def __str__(self):
#         return f"Affiliate: {self.user.full_name}"
