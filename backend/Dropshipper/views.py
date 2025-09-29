from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Case, When, Value, CharField
from django.db.models.functions import Coalesce
from django.utils import timezone
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.views import TokenObtainPairView

from django.db.models import Sum, F, DecimalField, Case, When, Value
from django.db.models.functions import Coalesce
from django.db import models
import random
from datetime import datetime

from django.core.files.base import ContentFile
import base64
import re
from django.db.models import Sum, F, Value, DecimalField
from django.db.models.functions import Coalesce
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal  # Import ajouté ici

from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password
from django.db.models import Max
from django.core.exceptions import ValidationError
import string
from django.http import JsonResponse
from django.db.models import Count, Subquery, OuterRef
import math
from django.db.models import Count, Q
from django.db import transaction

import uuid
import json
from django.db.models import Prefetch
from Backendkadi.utils import send_verification_email
from Backendkadi.models.commandes import  CustomOrder 
from Backendkadi.models.user import  User ,Client,Affiliate,Couturiere,UserDocuments
from Backendkadi.models.commandes import Order
from Backendkadi.models.modeles import  FashionModel
from Backendkadi.models.commandes import CustomOrder,Order
from Backendkadi.models.livraison import WilayaDelivery
from Backendkadi.models.promo import PromoCode
from Backendkadi.models.stock import StockVariantForFashionModels,StockVariantForCommands
from Backendkadi.models.socialAccountsLinkgroups import SocialAccountsLinkGroup
from Backendkadi.models.modeles import  FashionModel
from Backendkadi.models.modeles import ModelImage
from Backendkadi.models.commandes import CustomOrder,CustomOrderImage,Order
from Backendkadi.models.livraison import  WilayaDelivery
from Backendkadi.models.user  import User,Client,Dropshipper


#serializers
from .serializers import DropshipperSignupSerializer


class DropshipperSignupView(APIView):
    def post(self, request):
        serializer = DropshipperSignupSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            # Envoyer l'email de vérification
            send_verification_email(user.user)
            
            return Response(
                {
                    "success": "Inscription réussie. Un email de vérification a été envoyé.",
                    "user_id": user.user.id
                },
                status=status.HTTP_201_CREATED
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
    


@api_view(['GET'])
def check_status_dropshipper(request, email):
    try:
        # Vérifier que l'utilisateur existe
        user = get_object_or_404(User, email=email)
        
        # Vérifier que c'est bien un dropshipper
        if user.role != 'dropshipper':
            return Response(
                {"error": "Cet email ne correspond pas à un dropshipper"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Récupérer le profil dropshipper
        try:
            dropshipper = Dropshipper.objects.get(user=user)
        except Dropshipper.DoesNotExist:
            return Response(
                {"error": "Profil dropshipper introuvable pour cet utilisateur"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Déterminer le statut selon les conditions
        if dropshipper.is_accepted is None:
            status_value = "statuswaiting"
        elif dropshipper.is_accepted:
            if dropshipper.user.is_active:
                status_value = "actif"
            else:
                status_value = "notactif"
        else:
            # Cas où is_accepted = False (refusé)
            status_value = "refused"
        
        return Response({"status": status_value}, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {"error": f"Erreur serveur: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        
        
        

    
    
    
    
    
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_top_selling_models(request):
    
    if request.user.role != 'dropshipper':
        return Response(
            {"error": "Vous n'avez pas les permissions nécessaires pour effectuer cette action."},
            status=status.HTTP_403_FORBIDDEN
        )

    # Calculer la date il y a 30 jours
    thirty_days_ago = timezone.now() - timedelta(days=30)
    
    # Filtrer les FashionModel selon les critères
    models = FashionModel.objects.filter(
        state='accepted',
        price_per_piece_for_dropshipper__gt=0,  # Différent de 0
        orders__state='done',  # Commandes avec état 'done'
        orders__completed_at__gte=thirty_days_ago  # Commandes des 30 derniers jours
    ).distinct()
    
    # Annoter avec le nombre de commandes complétées
    models_with_count = models.annotate(
        completed_orders_count=Count(
            'orders',
            filter=Q(
                orders__state='done',
                orders__completed_at__gte=thirty_days_ago
            )
        )
    ).filter(completed_orders_count__gt=0)  # Exclure les modèles sans vente
    
    # Trier par nombre de commandes décroissant et limiter à 30
    top_models = models_with_count.order_by('-completed_orders_count')[:30]
    
    # Préparer la réponse
    result = []
    for model in top_models:
        # Récupérer les images
        images = [
            {
                'id': img.id,
                'image_url': request.build_absolute_uri(img.image.url) if img.image else None
            }
            for img in model.images.all()
        ]
        
        # Récupérer les variantes
        variants = [
            {
                'id': variant.id,
                'size': variant.size,
                'color': variant.color,
                'quantity': variant.quantity
            }
            for variant in model.variants.all()
        ]
        
        result.append({
            'name': model.name,
            'code': model.code,
            'description': model.description,
            'type': model.type,
            'price_per_piece_for_dropshipper': float(model.price_per_piece_for_dropshipper),
            'min_pieces_for_dropshipper': model.min_pieces_for_dropshipper,
            'images': images,
            'variants': variants,
            'completed_orders_count': model.completed_orders_count
        })
    
    return Response({
        'count': len(result),
        'results': result
    })