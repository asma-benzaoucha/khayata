from django.db import models
from django.core.validators import URLValidator, RegexValidator
from django.core.exceptions import ValidationError
from urllib.parse import urlparse

class SocialAccountsLinkGroup(models.Model):
        
    def validate_instagram_url(value):
        if value:
            parsed_url = urlparse(value)
            if not (parsed_url.netloc.endswith('instagram.com') or 
                   parsed_url.netloc.endswith('www.instagram.com')):
                raise ValidationError("L'URL doit être un lien Instagram valide")  
    def validate_facebook_url(value):
        if value:
            parsed_url = urlparse(value)
            if not (parsed_url.netloc.endswith('facebook.com') or 
                   parsed_url.netloc.endswith('www.facebook.com') or
                   parsed_url.netloc.endswith('fb.com')):
                raise ValidationError("L'URL doit être un lien Facebook valide")               
    def validate_whatsapp_group_url(value):
        if value:
            parsed_url = urlparse(value)
            # Les liens WhatsApp groups peuvent être de différents formats:
            # https://chat.whatsapp.com/...
            # https://whatsapp.com/group/...
            # https://www.whatsapp.com/group/...
            if not (parsed_url.netloc.endswith('chat.whatsapp.com') or 
                   parsed_url.netloc.endswith('whatsapp.com') or
                   parsed_url.netloc.endswith('www.whatsapp.com')):
                raise ValidationError("L'URL doit être un lien de groupe WhatsApp valide")
    phone_regex = RegexValidator(regex=r'^(05|06|07)\d{8}$',message="Le numéro doit être algérien (10 chiffres commençant par 05, 06 ou 07)")

      
    
      
    #les champs :     
    whatsapp = models.CharField( max_length=10, blank=True, null=True, validators=[phone_regex] )
    instagram = models.URLField(max_length=255,blank=True,null=True,validators=[URLValidator(), validate_instagram_url])
    facebook = models.URLField(max_length=255,blank=True,null=True,validators=[URLValidator(), validate_facebook_url])
    group_dropshipping = models.URLField(max_length=255,blank=True,null=True,validators=[URLValidator(), validate_whatsapp_group_url])
    group_investissement = models.URLField(max_length=255,blank=True,null=True,validators=[URLValidator(), validate_whatsapp_group_url])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)




    def __str__(self):
        return f"Liens sociaux - {self.id}"

    def clean(self):
        """Validation supplémentaire au niveau du modèle"""
        super().clean()
        
        # Validation du numéro WhatsApp
        if self.whatsapp and not self.whatsapp.isdigit():
            raise ValidationError({'whatsapp': "Le numéro ne doit contenir que des chiffres"})
        
        # Vérification que le numéro commence bien par 05, 06 ou 07
        if self.whatsapp and not self.whatsapp.startswith(('05', '06', '07')):
            raise ValidationError({'whatsapp': "Le numéro doit commencer par 05, 06 ou 07"})
        
        # Vérification de la longueur du numéro
        if self.whatsapp and len(self.whatsapp) != 10:
            raise ValidationError({'whatsapp': "Le numéro doit contenir exactement 10 chiffres"})

    def save(self, *args, **kwargs):
        """Nettoyage avant sauvegarde"""
        self.full_clean()
        super().save(*args, **kwargs)