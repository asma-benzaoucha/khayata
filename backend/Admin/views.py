
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
from .serializers import WilayaDeliverySerializer
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





from Backendkadi.models.commandes import  CustomOrder 
from Backendkadi.models.user import  User ,Client,Affiliate,Couturiere,UserDocuments
from Backendkadi.models.commandes import Order
from Backendkadi.models.modeles import  FashionModel
from Backendkadi.models.commandes import CustomOrder,Order
from Backendkadi.models.livraison import WilayaDelivery
from Backendkadi.models.promo import PromoCode
from Backendkadi.models.stock import StockVariantForFashionModels,StockVariantForCommands
from Backendkadi.models.socialAccountsLinkgroups import SocialAccountsLinkGroup

User = get_user_model()


#models
from Backendkadi.models.modeles import  FashionModel
from Backendkadi.models.modeles import ModelImage
from Backendkadi.models.commandes import CustomOrder,CustomOrderImage,Order
from Backendkadi.models.livraison import  WilayaDelivery
from Backendkadi.models.user  import User,Client,Dropshipper




#serializers
from Backendkadi.models.socialAccountsLinkgroups import SocialAccountsLinkGroup
from Client.serializers import SocialAccountsLinkGroupSerializer
from .serializers import BulkWilayaDeliverySerializer
from .serializers import FashionModelSerializer,FashionModelSerializer3, StockVariantForFashionModelsSerializer,StockVariantForCommandsSerializer,  StockVariantSerializerforCustomCommands,ModelImageSerializer











#create or update social links and whatsapp groups
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_or_update_social_links(request):
    """
    Crée ou met à jour les liens sociaux.
    Seul un administrateur peut effectuer cette action.
    """
    # Vérifier que l'utilisateur est admin
    if request.user.role != 'admin':
        return Response(
            {"error": "Accès refusé. Seuls les administrateurs peuvent effectuer cette action."},
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        # Vérifier s'il existe déjà un enregistrement
        social_links, created = SocialAccountsLinkGroup.objects.get_or_create(
            id=1  # Vous pouvez utiliser un ID spécifique ou une autre logique
        )
        
        # Sérialiser les données avec validation
        serializer = SocialAccountsLinkGroupSerializer(
            social_links, 
            data=request.data, 
            partial=not created  # partial=True pour la mise à jour, False pour la création
        )
        
        if serializer.is_valid():
            serializer.save()
            message = "créé avec succès" if created else "mis à jour avec succès"
            return Response(
                {"message": f"Liens sociaux {message}", "data": serializer.data},
                status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
            )
        else:
            return Response(
                {"error": "Données invalides", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
            
    except Exception as e:
        return Response(
            {"error": f"Erreur serveur: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        
    
#all orders of client and dropshiper 
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_orders(request):
    # Vérifier si l'utilisateur est admin
    if request.user.role != 'admin':
        return Response(
            {"error": "Accès non autorisé. Rôle administrateur requis."},
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        # Récupérer les commandes standard avec les relations
        standard_orders = Order.objects.select_related(
            'user', 'wilaya', 'fashion_model', 'promo_code'
        ).prefetch_related(
            'standard_command_details',
            'fashion_model__images'
        ).all()
        
        # Récupérer les commandes personnalisées avec les relations
        custom_orders = CustomOrder.objects.select_related(
            'user', 'wilaya'
        ).prefetch_related(
            'command_details',
            'custom_images'
        ).filter(command_type='personalized')
        
        # Préparer les données des commandes standard
        standard_data = []
        for order in standard_orders:
            # Format des détails de commande en triples
            details_triples = []
            for variant in order.standard_command_details.all():
                details_triples.append(f"({variant.size},{variant.color},{variant.quantity})")
            
            # Images du modèle
            images_urls = [img.image.url for img in order.fashion_model.images.all()]
            
            standard_data.append({
                'typecommande': 'standard',
                'id': order.id,
                'codecommande': order.code_order,
                'user': {
                    'role': order.user.role,
                    'email': order.user.email,
                    'full_name': order.user.full_name
                } if order.user else None,
                
                'dropshipper_client': {
        'id': order.dropshipper_client.id,
        'nom_client': order.dropshipper_client.nom_client,
        'dropshipper': {
            'id': order.dropshipper_client.dropshipper.id,
            'store_link': order.dropshipper_client.dropshipper.store_link,
            'phone_number': order.dropshipper_client.dropshipper.phone_number
        }
    } if order.dropshipper_client else None, 
                
                'state': order.state,
                'address': order.address,
                'wilaya': {
                    'wilaya_name': order.wilaya.wilaya_name if order.wilaya else None,
                    'delivery_price': float(order.wilaya.delivery_price) if order.wilaya else 0.0
                },
                'phone_number': order.phone_number,
                'standard_command_details': ','.join(details_triples),
                'promocode': {
                    'profit_percentage': float(order.promo_code.profit_percentage) if order.promo_code else None
                } if order.promo_code else None,
                'fashion_model': {
                    'name': order.fashion_model.name,
                    'code': order.fashion_model.code,
'price_per_piece_for_client': float(
            order.fashion_model.price_per_piece_for_dropshipper 
            if order.dropshipper_client 
            else order.fashion_model.price_per_piece_for_client
        ),                    'images': images_urls
                },
                'created_at': order.created_at
            })
        
        # Préparer les données des commandes personnalisées
        custom_data = []
        for order in custom_orders:
            # Calculer la quantité totale pour cette commande personnalisée
            total_quantity = sum(variant.quantity for variant in order.command_details.all())
            # Format des détails de commande en triples
            details_triples = []
            for variant in order.command_details.all():
                details_triples.append(f"({variant.size},{variant.color},{variant.quantity})")
            
            # Calcul des jours restants
            days_remaining = (order.deadline - timezone.now().date()).days
            days_remaining = max(0, days_remaining)  # Pas de valeurs négatives
            
            # Images de la commande personnalisée
            images_urls = [img.image.url for img in order.custom_images.all()]
            
            custom_data.append({
                'typecommande': 'custom',
                'id': order.id,
                'user': {
                    'role': order.user.role,
                    'email': order.user.email,
                    'full_name': order.user.full_name
                },
                'initial_price': float(order.initial_price) if order.initial_price else None,
                'command_type': order.command_type,
                'deadline_days_remaining': days_remaining,
                'state': order.state,
                'total_quantity': total_quantity,  
                'nameorder': order.nameorder,
                'codeorder': order.codeorder,
                'exactaddress': order.exactaddress,
                'wilaya': {
                    'wilaya_name': order.wilaya.wilaya_name,
                    'delivery_price': float(order.wilaya.delivery_price)
                },
                'numTelephone': order.numTelephone,
                'command_details': ','.join(details_triples),
                'images': images_urls,
                'created_at': order.created_at
            })
        
        # Combiner les deux listes
        all_orders = standard_data + custom_data
        
        # Trier les commandes : les états "done" et "cancelled" à la fin
        state_priority = {
            'inprogress':1,
            'pending': 1,
            'done': 3,
            'cancelled': 3,
            'Terminé': 3,  # Pour compatibilité
            'Annulé': 3,   # Pour compatibilité
            'En cours': 1  # Pour compatibilité
        }
        
        # Trier d'abord par priorité d'état, puis par date de création décroissante
        all_orders.sort(key=lambda x: (
            state_priority.get(x['state'], 2),  # Priorité par état
            x['created_at'].timestamp()        # Plus ancien d'abord
        ))
        
        # Convertir les dates en format string pour la réponse JSON
        for order in all_orders:
            order['created_at'] = order['created_at'].isoformat()
        
        return Response({
            'count': len(all_orders),
            'orders': all_orders
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {"error": f"Erreur lors de la récupération des commandes: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        
        
        


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_dropshippers_info(request):
    # Vérifier si l'utilisateur est admin
    if request.user.role != 'admin':
        raise PermissionDenied("Seuls les administrateurs peuvent accéder à cette ressource")
    
    try:
        # Récupérer le mois et l'année à partir des paramètres de requête (optionnel)
        current_month = request.GET.get('month', timezone.now().month)
        current_year = request.GET.get('year', timezone.now().year)
        
        # Convertir en entiers
        try:
            current_month = int(current_month)
            current_year = int(current_year)
        except (ValueError, TypeError):
            return Response({
                'error': 'Les paramètres month et year doivent être des nombres valides'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Calculer les dates de début et fin du mois
        start_date = timezone.make_aware(datetime(current_year, current_month, 1))
        if current_month == 12:
            end_date = timezone.make_aware(datetime(current_year + 1, 1, 1))
        else:
            end_date = timezone.make_aware(datetime(current_year, current_month + 1, 1))
        
        # Récupérer tous les dropshippers avec les conditions requises
        dropshippers = Dropshipper.objects.select_related('user').filter(
            user__role='dropshipper',
            user__email_verification_token__isnull=True,
            agreed_to_policy=True,
        )
        
        # Préparer les données de réponse
        dropshippers_data = []
        for dropshipper in dropshippers:
            # Initialiser le bénéfice à 0
            our_benifice = 0
            
            # Calculer le bénéfice seulement si le dropshipper est accepté et actif
            if dropshipper.is_accepted and dropshipper.user.is_active:
                # Récupérer toutes les commandes de ce dropshipper où l'état est devenu "done" pendant le mois spécifié
                orders = Order.objects.filter(
                    user=dropshipper.user,
                    updated_at__gte=start_date,  # Utiliser updated_at au lieu de created_at
                    updated_at__lt=end_date,
                    state='done'  # Seulement les commandes terminées
                ).prefetch_related('standard_command_details', 'fashion_model')
                
                # Calculer le bénéfice pour chaque commande
                for order in orders:
                    # Récupérer la quantité totale de la commande
                    total_quantity = order.standard_command_details.aggregate(
                        total_quantity=Sum('quantity')
                    )['total_quantity'] or 0
                    
                    # Calculer le bénéfice pour cette commande
                    # Bénéfice = prix dropshipper × quantité
                    dropshipper_price = order.fashion_model.price_per_piece_for_dropshipper
                    order_benefit = dropshipper_price * total_quantity
                    
                    our_benifice += order_benefit
            else:
                # Si le dropshipper n'est pas actif ou accepté, le bénéfice reste à 0
                our_benifice = 0
            
            dropshippers_data.append({
                'id': dropshipper.user.id,
                'full_name': dropshipper.user.full_name,
                'email': dropshipper.user.email,
                'phone_number': dropshipper.phone_number,
                'store_link': dropshipper.store_link,
                'is_accepted': dropshipper.is_accepted,
                'created_at': dropshipper.user.created_at,
                'is_active': dropshipper.user.is_active,
                'email_verified': dropshipper.user.email_verification_token is None,
                'ourbenificefromthisdropshipper': str(our_benifice)
            })
        
        return Response({
            'count': len(dropshippers_data),
            'dropshippers': dropshippers_data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'error': 'Une erreur est survenue lors de la récupération des données',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def bulk_update_wilaya_prices(request):
    # Vérifier si l'utilisateur est admin
    if not request.user.role == 'admin':
        return Response(
            {'error': 'Permission refusée. Seuls les administrateurs peuvent effectuer cette action.'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    serializer = BulkWilayaDeliverySerializer(data=request.data)
    
    if serializer.is_valid():
        try:
            result = serializer.save()
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': f'Erreur lors de la mise à jour: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Ou [IsAuthenticated] si vous voulez limiter l'accès
def get_all_wilayas(request):
    if not request.user.role == 'admin':
        return Response(
            {'error': 'Permission refusée. Seuls les administrateurs peuvent effectuer cette action.'},
            status=status.HTTP_403_FORBIDDEN
        )
    """
    Récupère toutes les wilayas avec leurs prix de livraison
    """
    try:
        # Récupérer toutes les wilayas
        wilayas = WilayaDelivery.objects.all().order_by('wilaya_name')
        
        # Sérialiser les données
        serializer = WilayaDeliverySerializer(wilayas, many=True)
        
        return Response({
            'count': wilayas.count(),
            'wilayas': serializer.data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': f'Erreur lors de la récupération des wilayas: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        
        
        
        
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def refuse_dropshipper(request, email):
    # Vérifier que l'utilisateur est un administrateur
    if request.user.role != 'admin':
        return Response(
            {"error": "Vous n'avez pas les permissions nécessaires pour effectuer cette action."},
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        # Récupérer l'utilisateur avec l'email fourni
        user = get_object_or_404(User, email=email)
        
        # Vérifier les conditions requises
        if (user.email_verification_token is not None or 
            not hasattr(user, 'dropshipper') or
            user.dropshipper.is_accepted is not None):
            
            return Response(
                {"error": "Cet utilisateur ne remplit pas les conditions pour être refusé."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        dropshipper = user.dropshipper
        dropshipper.refused_at = timezone.now()

        dropshipper.is_accepted = False
        user.is_active = False
        dropshipper.save()
        
        # Supprimer les dropshippers refusés il y a plus d'un mois
        month_ago = timezone.now() - timedelta(days=30)
        Dropshipper.objects.filter(
           is_accepted=False, 
          refused_at__lte=month_ago
        ).delete()
        
        
        return Response(
            {"message": f"Le dropshipper avec l'email {email} a été supprimé avec succès."},
            status=status.HTTP_200_OK
        )
            
    except Exception as e:
        return Response(
            {"error": f"Une erreur s'est produite: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        
        
        
        
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def accept_dropshipper(request, email):
    # Vérifier que l'utilisateur est un administrateur
    if request.user.role != 'admin':
        return Response(
            {"error": "Vous n'avez pas les permissions nécessaires pour effectuer cette action."},
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        # Récupérer l'utilisateur avec l'email fourni
        user = get_object_or_404(User, email=email)
        
        # Vérifier si l'utilisateur a un profil dropshipper
        if not hasattr(user, 'dropshipper'):
            return Response(
                {"error": "Cet utilisateur n'a pas de profil dropshipper."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        dropshipper = user.dropshipper
        
        # Vérifier les conditions requises
        if (user.email_verification_token is not None ):
            
            return Response(
                {"error": "Cet utilisateur ne remplit pas les conditions pour être accepté."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Mettre à jour les champs
        user.is_active = True
        user.save()
        
        dropshipper.is_accepted = True
        dropshipper.save()
        
        return Response(
            {
                "message": f"Le dropshipper avec l'email {email} a été accepté avec succès.",
                "data": {
                    "email": user.email,
                    "full_name": user.full_name,
                    "is_active": user.is_active,
                    "is_accepted": dropshipper.is_accepted,
                    "store_link": dropshipper.store_link,
                    "phone_number": dropshipper.phone_number
                }
            },
            status=status.HTTP_200_OK
        )
            
    except Exception as e:
        return Response(
            {"error": f"Une erreur s'est produite: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def activate_dropshipper_account_detailed(request, email):
    # Vérifier que l'utilisateur est un administrateur
    if request.user.role != 'admin':
        return Response(
            {"error": "Autorisation refusée. Seuls les administrateurs peuvent effectuer cette action."},
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        # Récupérer l'utilisateur avec l'email fourni
        user = get_object_or_404(User, email=email)
        
        # Vérifier si l'utilisateur a un profil dropshipper
        if not hasattr(user, 'dropshipper'):
            return Response(
                {"error": "Cet utilisateur n'a pas de profil dropshipper."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        dropshipper = user.dropshipper
        
        # Vérifications détaillées
        if user.email_verification_token is not None:
            return Response(
                {"error": "Cet utilisateur n'a pas encore vérifié son email."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        if not dropshipper.is_accepted:
            return Response(
                {"error": "Ce dropshipper n'a pas encore été accepté par l'administrateur."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        if user.is_active:
            return Response(
                {"error": "Ce compte dropshipper est déjà activé."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Activer le compte
        user.is_active = True
        user.save()
        
        return Response(
            {
                "message": f"Le compte dropshipper {email} a été activé avec succès.",
                "data": {
                    "email": user.email,
                    "full_name": user.full_name,
                    "is_active": user.is_active,
                    "is_accepted": dropshipper.is_accepted,
                    "store_link": dropshipper.store_link,
                    "phone_number": dropshipper.phone_number
                }
            },
            status=status.HTTP_200_OK
        )
            
    except User.DoesNotExist:
        return Response(
            {"error": "Utilisateur non trouvé."},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {"error": f"Erreur serveur: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        
        
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def deactivate_dropshipper_account(request, email):
    # Vérifier que l'utilisateur est un administrateur
    if request.user.role != 'admin':
        return Response(
            {"error": "Vous n'avez pas les permissions nécessaires pour effectuer cette action."},
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        # Récupérer l'utilisateur avec l'email fourni
        user = get_object_or_404(User, email=email)
        
        # Vérifier si l'utilisateur a un profil dropshipper
        if not hasattr(user, 'dropshipper'):
            return Response(
                {"error": "Cet utilisateur n'a pas de profil dropshipper."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        dropshipper = user.dropshipper
        
        # Vérifier les conditions requises
        if (user.email_verification_token is not None or 
            dropshipper.is_accepted is not True):
            
            return Response(
                {"error": "Cet utilisateur ne remplit pas les conditions pour être désactivé."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Désactiver le compte
        user.is_active = False
        user.save()
        
        return Response(
            {
                "message": f"Le compte dropshipper avec l'email {email} a été désactivé avec succès.",
                "data": {
                    "email": user.email,
                    "full_name": user.full_name,
                    "is_active": user.is_active,
                    "is_accepted": dropshipper.is_accepted,
                    "store_link": dropshipper.store_link,
                    "phone_number": dropshipper.phone_number
                }
            },
            status=status.HTTP_200_OK
        )
            
    except Exception as e:
        return Response(
            {"error": f"Une erreur s'est produite: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        
        


@api_view(['GET'])
def get_affiliates_info(request):
    today = timezone.now().date()
    
    # Récupérer tous les affiliés avec leurs informations
    affiliates = User.objects.filter(role='affiliate').prefetch_related(
        models.Prefetch(
            'promo_codes',
            queryset=PromoCode.objects.annotate(
                status=Case(
                    # Si la date de début est dans le futur -> "en attente"
                    When(start_date__gt=today, then=Value('en attente')),
                    # Si la date d'expiration est dans le passé -> "expiré"
                    When(expiration_date__lt=today, then=Value('expiré')),
                    # Sinon -> "active"
                    default=Value('active'),
                    output_field=models.CharField()
                )
            ).prefetch_related(
                models.Prefetch(
                    'models',
                    queryset=FashionModel.objects.all()
                ),
                models.Prefetch(
                    'standard_orders',
                    queryset=Order.objects.filter(state='done').annotate(
                        total_quantity=Coalesce(
                            Sum('standard_command_details__quantity'),
                            0,
                            output_field=DecimalField()
                        )
                    )
                )
            )
        )
    )
    
    result = []
    
    for affiliate in affiliates:
        # Récupérer le numéro de téléphone depuis le modèle Affiliate
        try:
            affiliate_profile = Affiliate.objects.get(user=affiliate)
            phone_number = affiliate_profile.phone_number
        except Affiliate.DoesNotExist:
            phone_number = None
        
        affiliate_data = {
            'full_name': affiliate.full_name,
            'email': affiliate.email,
            'phone_number': phone_number,
            'promo_codes': [],
            'total_benefice': 0
        }
        
        total_benefice = 0
        
        for promo_code in affiliate.promo_codes.all():
            # Calculer le bénéfice pour ce promo code
            benefice_promo = 0
            models_vendus = []
            
            # Récupérer les commandes "done" pour ce promo code
            # Ne considérer que les commandes si le code promo est actif
            
            orders_done = promo_code.standard_orders.all()
                
            for order in orders_done:
                    # Calculer la quantité totale pour cette commande
                    quantity = order.total_quantity
                    
                    # Calculer le bénéfice pour cette commande
                    if order.fashion_model and quantity > 0:
                        benefice_commande = (order.fashion_model.price_per_piece_for_client * (promo_code.profit_percentage / 100) * quantity)
                        benefice_promo += benefice_commande
                        
                        # Ajouter les informations du modèle vendu
                        model_info = {
                            'model_name': order.fashion_model.name,
                            'model_code': order.fashion_model.code,
                            'quantity': quantity,
                            'benefice_par_piece': order.fashion_model.price_per_piece_for_client * (promo_code.profit_percentage / 100)
                        }
                        models_vendus.append(model_info)
            
            
            total_benefice += benefice_promo
            
            # Récupérer les modèles affectés à ce promo code avec nom et code
            models_affectes = list(promo_code.models.values('name', 'code'))
            
            promo_data = {
                'code': promo_code.code,
                'profit_percentage': float(promo_code.profit_percentage),
                'discount_percentage':float(promo_code.discount_percentage),
                'expiration_date': promo_code.expiration_date,
                'start_date':promo_code.start_date,
                'status': promo_code.status,
                'models_affectes': models_affectes,  # Maintenant avec nom et code
                'models_vendus': models_vendus,
                'benefice_promo': round(benefice_promo, 2),
                'nombre_commandes_done': orders_done.count() if promo_code.status == 'active' else 0
            }
            
            affiliate_data['promo_codes'].append(promo_data)
        
        affiliate_data['total_benefice'] = round(total_benefice, 2)
        result.append(affiliate_data)
    
    return Response(result)


def generate_promo_code(length=8):
    """Génère un code promo aléatoire de la longueur spécifiée"""
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def generate_promo_code_api(request):
    # Vérifier que l'utilisateur est un administrateur
    if request.user.role != 'admin':
        return Response(
            {"error": "Permission refusée. Seuls les administrateurs peuvent générer des codes promo."},
            status=status.HTTP_403_FORBIDDEN
        )
    
    # Déterminer la longueur nécessaire
    base_length = 8
    total_existing_codes = PromoCode.objects.count()
    
    # Calculer la longueur minimale nécessaire
    # On cherche le plus petit n tel que 36^n >= total_existing_codes + 1
    # (36 caractères possibles : A-Z + 0-9)
    
    # Si on a dépassé la capacité pour la longueur de base
    max_possible_with_base_length = 36 ** base_length  # 36^8 possibilités
    
    if total_existing_codes >= max_possible_with_base_length:
        # Calculer la longueur nécessaire avec logarithme
        # length = ceil(log36(total_existing_codes + 1))
        length = math.ceil(math.log(total_existing_codes + 1, 36))
    else:
        length = base_length
    
    # Générer un code unique
    max_attempts = 20  # Augmenter le nombre de tentatives
    attempts = 0
    
    while attempts < max_attempts:
        code = generate_promo_code(length)
        
        # Vérifier si le code existe déjà
        if not PromoCode.objects.filter(code=code).exists():
            return Response({"promo_code": code}, status=status.HTTP_200_OK)
        
        attempts += 1
    
    # Si on n'a pas trouvé de code unique après plusieurs tentatives
    # Augmenter la longueur et réessayer une dernière fois
    length += 1
    code = generate_promo_code(length)
    
    # Vérifier une dernière fois
    if not PromoCode.objects.filter(code=code).exists():
        return Response({"promo_code": code}, status=status.HTTP_200_OK)
    
    return Response(
        {"error": "Impossible de générer un code unique après plusieurs tentatives."},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )
    
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_most_sold_models(request):
    if request.user.role != 'admin':
        return Response(
            {"error": "Permission refusée. Seuls les administrateurs peuvent générer des codes promo."},
            status=status.HTTP_403_FORBIDDEN
        )
    
    """
    API pour récupérer les modèles les plus vendus avec state='done'
    Retourne tous les modèles ayant le nombre maximum de ventes
    """
    
    # Compter le nombre de commandes 'done' pour chaque modèle
    sold_models = FashionModel.objects.annotate(
        done_orders_count=Count(
            'orders',
            filter=Q(orders__state='done')
        )
    ).filter(done_orders_count__gt=0).order_by('-done_orders_count')
    
    if not sold_models.exists():
        return Response({'most_sold_models': 'none'}, status=status.HTTP_200_OK)
    
    # Récupérer le nombre maximum de ventes
    max_sales_count = sold_models.first().done_orders_count
    
    # Filtrer tous les modèles ayant ce nombre maximum de ventes
    most_sold_models = sold_models.filter(done_orders_count=max_sales_count)
    
    # Sérialiser les résultats
    result = []
    for model in most_sold_models:
        result.append({
            'id': model.id,
            'name': model.name,
            'code': model.code,
            'type': model.type,
            'sales_count': model.done_orders_count,
            'price_per_piece_for_client': float(model.price_per_piece_for_client),
            'price_per_piece_for_dropshipper': float(model.price_per_piece_for_dropshipper),
            'description': model.description
        })
    
    return Response({'most_sold_models': result}, status=status.HTTP_200_OK)


    
    
    
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_most_active_couturiere(request):
    # Vérifier que l'utilisateur est un administrateur
    if request.user.role != 'admin':
        return Response(
            {"error": "Vous n'avez pas les permissions nécessaires."},
            status=403
        )
    
    # Filtrer d'abord les modèles qui ont un owner (couturière)
    models_with_owner = FashionModel.objects.filter(
        owner__isnull=False,
        owner__role='couturiere',
        owner__is_active=True
    )
    
    # Vérifier s'il existe des modèles avec owner couturière
    if not models_with_owner.exists():
        return Response({
            "message": "Aucun modèle n'appartient à une couturière.",
            "has_active_couturiere": False
        })
    
    # Compter les ventes (orders avec state='done') pour ces modèles
    models_sales = models_with_owner.annotate(
        sales_count=Count('orders', filter=Q(orders__state='done'))
    ).filter(sales_count__gt=0).order_by('-sales_count')
    
    # Si aucune vente n'a été réalisée pour les modèles avec couturière
    if not models_sales.exists():
        return Response({
            "message": "Aucune vente n'a été réalisée pour les modèles des couturières.",
            "has_active_couturiere": False
        })
    
    # Trouver le nombre maximum de ventes
    max_sales = models_sales.first().sales_count
    
    # Récupérer tous les modèles avec le nombre maximum de ventes
    top_models = models_sales.filter(sales_count=max_sales)
    
    # Récupérer les couturières propriétaires de ces modèles (filtrées et actives)
    couturieres_data = []
    couturiere_ids = set()
    
    for model in top_models:
        # Vérifier que la couturière est acceptée
        if (hasattr(model.owner, 'couturiere') and 
            model.owner.couturiere.is_accepted):
            
            # Éviter les doublons
            if model.owner.id not in couturiere_ids:
                couturiere_ids.add(model.owner.id)
                
                couturiere = model.owner.couturiere
                # Récupérer tous les modèles de cette couturière qui ont max_sales
                owner_top_models = top_models.filter(owner=model.owner)
                
                couturieres_data.append({
                    "id": model.owner.id,
                    "full_name": model.owner.full_name,
                    "email": model.owner.email,
                    "address": couturiere.address,
                    "phone_number": couturiere.phone_number,
                    "sales_count": max_sales,
                    "top_models": [
                        {
                            "model_id": m.id,
                            "model_name": m.name,
                            "model_code": m.code,
                            "sales_count": m.sales_count
                        }
                        for m in owner_top_models
                    ]
                })
    
    # Cas où aucun modèle top n'appartient à une couturière valide (is_accepted=True)
    if not couturieres_data:
        return Response({
            "message": "Aucune couturière active trouvée. Les couturières des modèles les plus vendus ne sont pas acceptées.",
            "has_active_couturiere": False
        })
    
    # Si une seule couturière a le plus de ventes
    if len(couturieres_data) == 1:
        return Response({
            "most_active_couturiere": couturieres_data[0],
            "is_tie": False,
            "has_active_couturiere": True
        })
    
    # Si plusieurs couturières ont le même nombre de ventes maximum
    return Response({
        "most_active_couturieres": couturieres_data,
        "is_tie": True,
        "sales_count": max_sales,
        "has_active_couturiere": True
    })
    
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_most_active_affiliate(request):
    try:
        # Récupérer tous les affiliés actifs avec email vérifié
        active_affiliates = User.objects.filter(
            role='affiliate',
            is_active=True,
            email_verification_token__isnull=True
        )
        
        if not active_affiliates.exists():
            return Response({
                'message': 'Aucun affilié actif trouvé',
                'most_active_affiliates': []
            })
        
        affiliate_stats = []
        
        for affiliate in active_affiliates:
            # Récupérer tous les codes promo valides de cet affilié
            today = timezone.now().date()
            valid_promo_codes = PromoCode.objects.filter(
                affiliate=affiliate,
                start_date__lte=today,
                expiration_date__gte=today
            )
            
            total_orders = 0
            
            # Compter les commandes "done" pour chaque code promo valide
            for promo_code in valid_promo_codes:
                orders_count = Order.objects.filter(
                    promo_code=promo_code,
                    state='done'
                ).count()
                total_orders += orders_count
                
            if total_orders == 0:
                 continue
            
            # Récupérer le numéro de téléphone de l'affilié
            try:
                affiliate_profile = Affiliate.objects.get(user=affiliate)
                phone_number = affiliate_profile.phone_number
            except Affiliate.DoesNotExist:
                phone_number = None
            
            affiliate_stats.append({
                'affiliate_id': affiliate.id,
                'full_name': affiliate.full_name,
                'phone_number': phone_number,
                'total_orders': total_orders
            })
        
        # Trouver le nombre maximum de commandes
        if not affiliate_stats:
            return Response({
                'message': 'Aucune donnée d\'utilisation trouvée',
                'most_active_affiliates': []
            })
        
        max_orders = max(affiliate['total_orders'] for affiliate in affiliate_stats)
        
        # Filtrer les affiliés avec le nombre maximum de commandes
        most_active_affiliates = [
            affiliate for affiliate in affiliate_stats 
            if affiliate['total_orders'] == max_orders
        ]
        
        return Response({
            'message': f'Affilié(s) le(s) plus actif(s) trouvé(s) avec {max_orders} commandes',
            'most_active_affiliates': most_active_affiliates
        })
        
    except Exception as e:
        return Response({
            'error': f'Une erreur s\'est produite: {str(e)}'
        }, status=500)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_new_affiliate(request):
    # Vérifier que l'utilisateur est admin
    if request.user.role != 'admin':
        return Response(
            {'error': 'Accès refusé. Seuls les administrateurs peuvent créer des affiliés.'},
            status=status.HTTP_403_FORBIDDEN
        )

    try:
        data = request.data
        
        # Validation des données requises
        required_fields = ['full_name', 'email', 'password', 
                          'promo_code', 'profit_percentage', 'discount_percentage',
                          'start_date', 'expiration_date', 'model_codes','phoneNumber']
        
        for field in required_fields:
            if field not in data:
                return Response(
                    {'error': f'Le champ {field} est requis.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Vérifier si l'email existe déjà
        if User.objects.filter(email=data['email']).exists():
            return Response(
                {'error': 'Cet email est déjà utilisé.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Vérifier si le code promo existe déjà
        if PromoCode.objects.filter(code=data['promo_code']).exists():
            return Response(
                {'error': 'Ce code promo existe déjà.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validation du mot de passe
        password = data['password']
        if len(password) < 8:
            return Response(
                {'error': 'Le mot de passe doit contenir au moins 8 caractères.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validation des dates
        start_date = timezone.datetime.strptime(data['start_date'], '%Y-%m-%d').date()
        expiration_date = timezone.datetime.strptime(data['expiration_date'], '%Y-%m-%d').date()
        today = timezone.now().date()
        
        # Vérifier que start_date est dans le futur
        if start_date < today:
            return Response(
                {'error': 'La date de début doit être dans le futur.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if expiration_date <= start_date:
            return Response(
                {'error': 'La date d\'expiration doit être postérieure à la date de début.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Vérifier que les modèles existent et sont acceptés
        model_codes = data['model_codes']
        if not isinstance(model_codes, list):
            return Response(
                {'error': 'model_codes doit être une liste de codes.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        fashion_models = FashionModel.objects.filter(code__in=model_codes, state='accepted')
        if len(fashion_models) != len(model_codes):
            # Trouver les codes qui n'existent pas ou ne sont pas acceptés
            existing_codes = set(fashion_models.values_list('code', flat=True))
            missing_codes = set(model_codes) - existing_codes
            return Response(
                {'error': f'Modèles non trouvés ou non acceptés: {list(missing_codes)}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Vérifier qu'aucun modèle n'est déjà affecté à un code promo
        already_assigned_models = []
        for fashion_model in fashion_models:
            if fashion_model.promo_code is not None:
                already_assigned_models.append(fashion_model.code)
        
        if already_assigned_models:
            return Response(
                {'error': f'Les modèles suivants sont déjà affectés à un code promo: {already_assigned_models}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Créer l'utilisateur affilié
        user = User.objects.create(
            full_name=data['full_name'],
            email=data['email'],
            password=make_password(password),
            role='affiliate',
            email_verification_token=None,
            is_active=True  # Activer directement car créé par admin
        )

        # Créer le profil affilié
        affiliate = Affiliate.objects.create(
            user=user,
            phone_number=data["phoneNumber"]
        )

        # Créer le code promo
        promo_code = PromoCode.objects.create(
            code=data['promo_code'],
            affiliate=user,
            profit_percentage=data['profit_percentage'],
            discount_percentage=data['discount_percentage'],
            start_date=start_date,
            expiration_date=expiration_date
        )

        # Lier les modèles au code promo
        for fashion_model in fashion_models:
            fashion_model.promo_code = promo_code
            fashion_model.save()

        return Response({
            'message': 'Affilié créé avec succès',
            'user_id': user.id,
            'affiliate_id': affiliate.id,
            'promo_code_id': promo_code.id,
            'promo_code': promo_code.code,
            'linked_models': [model.code for model in fashion_models],
            'discount_percentage': float(data['discount_percentage'])
        }, status=status.HTTP_201_CREATED)

    except ValidationError as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {'error': f'Erreur serveur: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        
        
        
        
        
        
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def rework_with_affiliate(request, email):
    # Vérifier que l'utilisateur est admin
    if request.user.role != 'admin':
        return Response(
            {'error': 'Accès refusé. Seuls les administrateurs peuvent modifier des affiliés.'},
            status=status.HTTP_403_FORBIDDEN
        )

    try:
        data = request.data
        
        # Validation des données requises
        required_fields = ['promo_code', 'profit_percentage', 'discount_percentage',
                          'start_date', 'expiration_date', 'model_codes']
        
        for field in required_fields:
            if field not in data:
                return Response(
                    {'error': f'Le champ {field} est requis.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Vérifier que l'affilié existe
        try:
            affiliate_user = User.objects.get(email=email, role='affiliate')
        except User.DoesNotExist:
            return Response(
                {'error': f'Aucun affilié trouvé avec l\'email {email}'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Vérifier si le nouveau code promo existe déjà (quel que soit l'affilié)
        if PromoCode.objects.filter(code=data['promo_code']).exists():
            return Response(
                {'error': 'Ce code promo existe déjà.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validation des dates
        start_date = timezone.datetime.strptime(data['start_date'], '%Y-%m-%d').date()
        expiration_date = timezone.datetime.strptime(data['expiration_date'], '%Y-%m-%d').date()
        today = timezone.now().date()
        
        # Vérifier que start_date est dans le futur
        if start_date < today:
            return Response(
                {'error': 'La date de début doit être dans le futur.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if expiration_date <= start_date:
            return Response(
                {'error': 'La date d\'expiration doit être postérieure à la date de début.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Vérifier que les modèles existent et sont acceptés
        model_codes = data['model_codes']
        if not isinstance(model_codes, list):
            return Response(
                {'error': 'model_codes doit être une liste de codes.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        fashion_models = FashionModel.objects.filter(code__in=model_codes, state='accepted')
        if len(fashion_models) != len(model_codes):
            # Trouver les codes qui n'existent pas ou ne sont pas acceptés
            existing_codes = set(fashion_models.values_list('code', flat=True))
            missing_codes = set(model_codes) - existing_codes
            return Response(
                {'error': f'Modèles non trouvés ou non acceptés: {list(missing_codes)}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Vérifier qu'aucun modèle n'est déjà affecté à un code promo (quel que soit l'affilié)
        already_assigned_models = FashionModel.objects.filter(
            code__in=model_codes,
            promo_code__isnull=False
        ).values_list('code', flat=True)

        if already_assigned_models:
            return Response(
                {'error': f'Les modèles suivants sont déjà affectés à un code promo: {list(already_assigned_models)}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Créer un NOUVEAU code promo (ne pas mettre à jour l'existant)
        promo_code = PromoCode.objects.create(
            code=data['promo_code'],
            affiliate=affiliate_user,
            profit_percentage=data['profit_percentage'],
            discount_percentage=data['discount_percentage'],
            start_date=start_date,
            expiration_date=expiration_date
        )

        # Lier les nouveaux modèles au NOUVEAU code promo
        # (les anciens codes promo de l'affilié restent inchangés)
        for fashion_model in fashion_models:
            fashion_model.promo_code = promo_code
            fashion_model.save()

        return Response({
            'message': 'Nouveau code promo créé pour l\'affilié avec succès',
            'affiliate_email': affiliate_user.email,
            'affiliate_name': affiliate_user.full_name,
            'promo_code_id': promo_code.id,
            'promo_code': promo_code.code,
            'linked_models': [model.code for model in fashion_models],
            'profit_percentage': float(data['profit_percentage']),
            'discount_percentage': float(data['discount_percentage']),
            'start_date': data['start_date'],
            'expiration_date': data['expiration_date'],
            'total_promo_codes': PromoCode.objects.filter(affiliate=affiliate_user).count()
        }, status=status.HTTP_201_CREATED)

    except ValidationError as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {'error': f'Erreur serveur: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        
        
        
        
        
@api_view(['GET'])
def get_models_not_affected_toaprmocode(request):
    # Filtrer les modèles acceptés sans code promo
    models = FashionModel.objects.filter(
        state='accepted',
        promo_code__isnull=True
    )
    
    # Sérialiser les données
    data = []
    for model in models:
        data.append({
            'id': model.id,
            'name': model.name,
            'code': model.code,
            
        })
    
    return Response(data)












def update_variants(fashion_model, variants_data):
    """
    Met à jour les variantes du modèle - version corrigée
    """
    with transaction.atomic():
        # Créer une liste pour stocker les nouvelles variantes
        new_variants = []
        
        for variant_data in variants_data:
            size = variant_data.get('size', '').strip()
            color = variant_data.get('color', '').strip()
            quantity = variant_data.get('quantity', 0)
            
            if not size or not color:
                continue
                
            try:
                quantity = int(quantity)
                if quantity < 0:
                    quantity = 0
            except (ValueError, TypeError):
                quantity = 0
            
            # Vérifier si une variante avec la même taille et couleur existe déjà
            existing_variants = StockVariantForFashionModels.objects.filter(
                size=size,
                color=color
            )
            
            if existing_variants.exists():
                # Utiliser la première variante existante
                variant = existing_variants.first()
                variant.quantity = quantity
                variant.save()
            else:
                # Créer une nouvelle variante
                variant = StockVariantForFashionModels.objects.create(
                    size=size,
                    color=color,
                    quantity=quantity
                )
            
            new_variants.append(variant)
        
        # Mettre à jour les variantes du modèle
        fashion_model.variants.set(new_variants)

def handle_new_images(fashion_model, new_images):
    """
    Ajoute de nouvelles images sans écraser les existantes
    """
    for image_file in new_images:
        if image_file:
            ModelImage.objects.create(
                fashion_model=fashion_model,
                image=image_file
            )


        
        
        
        

        
        

            
            
            
            
            
            
            
            
            
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def refuse_command(request, command_type, command_code):
    if not request.user.is_staff:
            return Response(
                {'error': 'Permission denied. Admin access required.'},
                status=status.HTTP_403_FORBIDDEN
            )
    """
    Refuse une commande en fonction de son type (standard ou custom)
    URL: /adminapi/refusecommand/<command_type>/<command_code>/
    """
   
    if command_type not in ['standard', 'custom']:
        return Response(
            {"error": "Le type de commande doit être 'standard' ou 'custom'"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        if command_type == 'custom':
            # Recherche de la commande custom
            custom_order = get_object_or_404(CustomOrder, codeorder=command_code)
            
            # Vérification si la commande peut être annulée
            if custom_order.state == 'cancelled':
                return Response(
                    {"message": "Cette commande est déjà annulée"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Mise à jour du statut
            custom_order.state = 'cancelled'
            custom_order.completed_at=timezone.now()
            custom_order.save()
            
            return Response(
                {"message": f"Commande custom {command_code} a été annulée avec succès"},
                status=status.HTTP_200_OK
            )
            
        else:  # command_type == 'standard'
            # Recherche de la commande standard
            standard_order = get_object_or_404(Order, code_order=command_code)
            
            # Vérification si la commande peut être annulée
            if standard_order.state == 'cancelled':
                return Response(
                    {"message": "Cette commande est déjà annulée"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Mise à jour du statut
            standard_order.state = 'cancelled'
            standard_order.completed_at=timezone.now()
            standard_order.save()
            
            return Response(
                {"message": f"Commande standard {command_code} a été annulée avec succès"},
                status=status.HTTP_200_OK
            )
            
    except Exception as e:
        return Response(
            {"error": f"Une erreur s'est produite: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        
        
        
        
        
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_order_status_versinprogresspourcommandestandard(request, code_order):
    if not request.user.is_staff:
            return Response(
                {'error': 'Permission denied. Admin access required.'},
                status=status.HTTP_403_FORBIDDEN
            )
    try:
       
        # Récupérer la commande par son code
        order = get_object_or_404(Order, code_order=code_order)
        
        # Vérifier si le statut peut être changé vers "inprogress"
        if order.state != 'inprogress':
            # Mettre à jour le statut
            order.state = 'inprogress'
            order.save()
            
            return Response(
                {"message": f"Statut de la commande {code_order} mis à jour vers 'inprogress'."},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"message": f"La commande {code_order} est déjà en statut 'inprogress'."},
                status=status.HTTP_200_OK
            )
            
    except Exception as e:
        return Response(
            {"error": f"Erreur lors de la mise à jour: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        
        
        
        
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_custom_order_statusversinprogress(request, codeorder, new_price):
    if not request.user.is_staff:
            return Response(
                {'error': 'Permission denied. Admin access required.'},
                status=status.HTTP_403_FORBIDDEN
            )
    try:
       
        
        # Convertir le nouveau prix en décimal
        new_price_decimal = Decimal(new_price)
        
        # Récupérer la commande par son code
        order = get_object_or_404(CustomOrder, codeorder=codeorder)
        
        # Mettre à jour le statut et le prix
        order.state = 'inprogress'
        order.initial_price = new_price_decimal
        order.save()
        
        return Response(
            {
                "message": f"Commande {codeorder} mise à jour avec succès.",
                "new_status": "inprogress",
                "new_price": float(new_price_decimal)
            },
            status=status.HTTP_200_OK
        )
            
    except ValueError:
        return Response(
            {"error": "Le prix doit être un nombre valide."},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {"error": f"Erreur lors de la mise à jour: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        
        
        
        
        
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def make_standard_command_done(request, model_code, order_code):
    if not request.user.is_staff:
        return Response(
            {'error': 'Permission denied. Admin access required.'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        # Récupérer la commande et le modèle
        order = get_object_or_404(Order, code_order=order_code)
        fashion_model = get_object_or_404(FashionModel, code=model_code)
        
        # Vérifier que le modèle correspond à la commande
        if order.fashion_model != fashion_model:
            return Response(
                {"error": "Le modèle ne correspond pas à cette commande."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Vérifier que la commande est dans un état valide pour être traitée
        if order.state != 'pending' and order.state != 'inprogress':
            return Response(
                {"error": "La commande n'est pas dans un état valide pour être marquée comme terminée."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Récupérer les variantes directement depuis la relation ManyToMany
        variants = order.standard_command_details.all()
        
        if not variants.exists():
            return Response(
                {"error": "Aucune variante trouvée pour cette commande."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Traiter la transaction de manière atomique
        with transaction.atomic():
            # Mettre à jour l'état de la commande
            order.state = 'done'
            order.completed_at = timezone.now()  

            order.save()
            
            # Traiter chaque variante de la commande
            for variant in variants:
                # Trouver la variante correspondante dans le modèle
                try:
                    stock_variant = fashion_model.variants.get(
                        size=variant.size, 
                        color=variant.color,
                        
                    )
                except StockVariantForCommands.DoesNotExist:
                    return Response(
                        {"error": f"Variante {variant.size}/{variant.color} non trouvée pour ce modèle."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                # Diminuer la quantité
                stock_variant.quantity -= variant.quantity
                
                if stock_variant.quantity == 0:
                    # Supprimer la variante si la quantité devient 0
                    stock_variant.delete()
                else:
                    stock_variant.save()
            
            # Vérifier si le modèle n'a plus de variantes
            remaining_variants = fashion_model.variants.all()
            if not remaining_variants.exists():
                fashion_model.state = 'notvisible'
                fashion_model.completed_at=timezone.now()
                fashion_model.save()
            else:
                # Vérifier si toutes les variantes ont une quantité de 0
                total_quantity = sum(v.quantity for v in remaining_variants)
                if total_quantity == 0:
                    fashion_model.state = 'notvisible'
                    fashion_model.completed_at=timezone.now()
                    fashion_model.save()
      
            try:
             two_months_ago = timezone.now() - timezone.timedelta(days=60)
             old_completed_orders = Order.objects.filter(
                state__in=['done', 'refused'],
                completed_at__lt=two_months_ago
             )
             old_completed_orders.delete()
            except Exception as e:
             print(f"Erreur lors du nettoyage des anciennes commandes: {str(e)}")
            
              
        return Response(
            {"message": "Commande marquée comme terminée et stocks mis à jour avec succès."},
            status=status.HTTP_200_OK
        )
    
    except Exception as e:
        return Response(
            {"error": f"Une erreur s'est produite: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        
        
        
        
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_model_variants(request, model_code):
    if not request.user.is_staff:
        return Response(
            {'error': 'Permission denied. Admin access required.'},
            status=status.HTTP_403_FORBIDDEN
        )
    try:
        # Récupérer le modèle par son code
        fashion_model = FashionModel.objects.get(code=model_code)
        
        # Récupérer les variantes du body de la requête
        body = json.loads(request.body)
        order_variants = body.get('variants', [])
        
        if not order_variants:
            return JsonResponse({
                'error': 'Aucune variante fournie dans le body'
            }, status=400)
        
        # Récupérer toutes les variantes du modèle
        model_variants = fashion_model.variants.all()
        
        response_data = {
            'isOkay': True,
            'model_code': model_code,
            'model_name': fashion_model.name,
            'variants_analysis': [],
            'missing_variants': []
        }
        
        # Vérifier chaque variante de la commande
        for order_variant in order_variants:
            size = order_variant.get('size')
            color = order_variant.get('color')
            order_quantity = order_variant.get('quantity')
            
            if not all([size, color, order_quantity]):
                return JsonResponse({
                    'error': f'Variante incomplète: {order_variant}'
                }, status=400)
            
            # Chercher la variante correspondante dans le modèle
            matching_variant = None
            for model_variant in model_variants:
                if (model_variant.size == size and 
                    model_variant.color == color):
                    matching_variant = model_variant
                    break
            
            variant_analysis = {
                'size': size,
                'color': color,
                'order_quantity': order_quantity,
                'exists_in_model': False,
                'available_quantity': 0,
                'sufficient_quantity': False,
                'missing_quantity': 0,
                'needs_addition': False
            }
            
            if matching_variant:
                variant_analysis['exists_in_model'] = True
                variant_analysis['available_quantity'] = matching_variant.quantity
                
                # Vérifier si la quantité est suffisante
                if matching_variant.quantity >= order_quantity:
                    variant_analysis['sufficient_quantity'] = True
                else:
                    variant_analysis['sufficient_quantity'] = False
                    variant_analysis['missing_quantity'] = order_quantity - matching_variant.quantity
                    variant_analysis['needs_addition'] = True
                    response_data['isOkay'] = False
                    
            else:
                # La variante n'existe pas du tout dans le modèle
                variant_analysis['needs_addition'] = True
                variant_analysis['missing_quantity'] = order_quantity
                response_data['isOkay'] = False
                
                # Ajouter aux variantes manquantes
                response_data['missing_variants'].append({
                    'size': size,
                    'color': color,
                    'required_quantity': order_quantity
                })
            
            response_data['variants_analysis'].append(variant_analysis)
        
        return JsonResponse(response_data)
        
    except FashionModel.DoesNotExist:
        return JsonResponse({
            'error': f'Modèle avec le code {model_code} non trouvé ou non accepté'
        }, status=404)
        
    except json.JSONDecodeError:
        return JsonResponse({
            'error': 'Body JSON invalide'
        }, status=400)
        
    except Exception as e:
        return JsonResponse({
            'error': f'Erreur serveur: {str(e)}'
        }, status=500)
        
        
        
        
        
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])        
def modify_model_variants(request, model_code):
    if not request.user.is_staff:
        return Response(
            {'error': 'Permission denied. Admin access required.'},
            status=status.HTTP_403_FORBIDDEN
        )
    try:
        # Récupérer le modèle par son code
        fashion_model = FashionModel.objects.get(code=model_code)
        
        # Récupérer les variantes à modifier/ajouter depuis le body
        body = json.loads(request.body)
        variants_to_modify = body.get('variants', [])
        
        if not variants_to_modify:
            return JsonResponse({
                'error': 'Aucune variante fournie dans le body'
            }, status=400)
        
        response_data = {
            'model_code': model_code,
            'model_name': fashion_model.name,
            'modified_variants': [],
            'created_variants': [],
            'errors': []
        }
        
        # Utiliser une transaction pour garantir l'intégrité des données
        with transaction.atomic():
            # Récupérer toutes les variantes existantes du modèle
            existing_variants = fashion_model.variants.all()
            
            for variant_data in variants_to_modify:
                size = variant_data.get('size')
                color = variant_data.get('color')
                quantity_to_add = variant_data.get('quantity')
                
                if not all([size, color, quantity_to_add]):
                    response_data['errors'].append({
                        'variant': variant_data,
                        'error': 'Données incomplètes (size, color, quantity requis)'
                    })
                    continue
                
                if quantity_to_add <= 0:
                    response_data['errors'].append({
                        'variant': variant_data,
                        'error': 'La quantité doit être positive'
                    })
                    continue
                
                # Chercher si la variante existe déjà dans le modèle
                existing_variant = None
                for variant in existing_variants:
                    if variant.size == size and variant.color == color:
                        existing_variant = variant
                        break
                
                if existing_variant:
                    # Mettre à jour la quantité existante
                    old_quantity = existing_variant.quantity
                    existing_variant.quantity += quantity_to_add
                    existing_variant.save()
                    
                    response_data['modified_variants'].append({
                        'size': size,
                        'color': color,
                        'old_quantity': old_quantity,
                        'added_quantity': quantity_to_add,
                        'new_quantity': existing_variant.quantity
                    })
                    
                
                else:
    # Créer une nouvelle variante directement liée au modèle
                 new_variant = StockVariantForFashionModels.objects.create(
                 fashion_model=fashion_model,
                 size=size,
                 color=color,
                 quantity=quantity_to_add
                 )
    
                response_data['created_variants'].append({
                'size': size,
                'color': color,
                'quantity': quantity_to_add
                })
                        
                
        # Rafraîchir les données du modèle
        fashion_model.refresh_from_db()      
        return JsonResponse(response_data)
        
    except FashionModel.DoesNotExist:
        return JsonResponse({
            'error': f'Modèle avec le code {model_code} non trouvé'
        }, status=404)
        
    except json.JSONDecodeError:
        return JsonResponse({
            'error': 'Body JSON invalide'
        }, status=400)
        
    except Exception as e:
        return JsonResponse({
            'error': f'Erreur serveur: {str(e)}'
        }, status=500)
        
        
        
        
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def make_custom_command_done(request, ordercode):
    # Vérifier que l'utilisateur est un administrateur 
    if request.user.role != 'admin':
        return Response(
            {"error": "Accès refusé. Seuls les administrateurs peuvent effectuer cette action."},
            status=status.HTTP_403_FORBIDDEN
        )
    
    # Récupérer la commande par son code
    custom_order = get_object_or_404(CustomOrder, codeorder=ordercode)
    
    # Vérifier si l'état actuel est "pending" (En attente)
    if custom_order.state == 'waiting':
        try:
            # Charger le corps de la requête JSON
            data = json.loads(request.body)
            price = data.get('price')
            
            # Vérifier si le prix est fourni
            if price is None:
                return Response(
                    {"error": "Le prix est requis pour les commandes en attente"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Convertir et valider le prix
            try:
                price = Decimal(price)
                if price <= 0:
                    raise ValueError
            except (ValueError, TypeError):
                return Response(
                    {"error": "Le prix doit être un nombre positif"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Mettre à jour le prix initial
            custom_order.initial_price = price
            
        except json.JSONDecodeError:
            return Response(
                {"error": "Corps de la requête JSON invalide"},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    # Mettre à jour l'état de la commande vers "done"
    custom_order.state = 'done'
    custom_order.completed_at = timezone.now()  

    custom_order.save()
    
    
    
    two_months_ago = timezone.now() - timedelta(days=60)
    old_orders = CustomOrder.objects.filter(
    command_type='personalized',
    state__in=['done', 'cancelled'],  
    completed_at__lt=two_months_ago
    )
    old_orders.delete()
    
    return Response(
        {
            "message": "État de la commande mis à jour avec succès",
            "order_code": custom_order.codeorder,
            "new_state": custom_order.state,
            "initial_price": custom_order.initial_price
        },
        status=status.HTTP_200_OK
    )
    
    
    
@api_view(['GET'])
@permission_classes([IsAuthenticated]) 
def list_couturieres(request):
    if request.user.role != 'admin':
        return Response(
            {"error": "Accès refusé. Seuls les administrateurs peuvent effectuer cette action."},
            status=status.HTTP_403_FORBIDDEN
        )
    try:
        # Construction de la requête avec préchargement optimisé
        couturieres = Couturiere.objects.select_related('user').prefetch_related(
            Prefetch(
                'user__documents',
                queryset=UserDocuments.objects.all(),
                to_attr='prefetched_documents'
            )
        ).filter(
            user__email_verification_token__isnull=True,
            user__role='couturiere'
        ).filter(
            models.Q(is_accepted=True) | models.Q(is_accepted__isnull=True)
        ).order_by('user__created_at')  # Tri par date de création croissante
        
        # Préparation des données
        result = []
        for couturiere in couturieres:
            data = {
                'id': couturiere.id,
                'user_id': couturiere.user.id,
                'full_name': couturiere.user.full_name,
                'email': couturiere.user.email,
                'phonenumber': couturiere.phone_number,
                'isaccepted': couturiere.is_accepted,
                'isactive': couturiere.user.is_active,
                'created_at': couturiere.user.created_at.strftime('%d-%m-%Y') if couturiere.user.created_at else None,
                'address': couturiere.address,
                'documents': []
            }
            
            # Ajout des documents si nécessaire
            if( (couturiere.is_accepted  is None or couturiere.is_accepted is True)  and hasattr(couturiere.user, 'prefetched_documents')):
                for doc in couturiere.user.prefetched_documents:
                    data['documents'].append({
                        'document_id': doc.id,
                        'file_url': request.build_absolute_uri(doc.nom.url) if doc.nom else None,
                        'file_name': doc.nom.name.split('/')[-1] if doc.nom else None,
                        'uploaded_at': doc.uploaded_at.isoformat() if doc.uploaded_at else None
                    })
            
            result.append(data)
        
        return JsonResponse({
            'status': 'success',
            'data': result,
            'total': len(result)
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Erreur lors de la récupération des données: {str(e)}'
        }, status=500)
        
        
        
        
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_couturiere_status(request, id):
    if request.user.role != 'admin':
        return Response(
            {"error": "Accès refusé. Seuls les administrateurs peuvent effectuer cette action."},
            status=status.HTTP_403_FORBIDDEN)
    
    try:
        # Récupérer la couturière par son ID utilisateur
        couturiere = get_object_or_404(Couturiere, id=id)
        
        # Vérifier si le body contient isaccepted
        if 'isaccepted' not in request.data:
            return Response(
                {'error': 'Le champ isaccepted est requis'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        new_status = request.data['isaccepted']
        
        # Mettre à jour les statuts selon la logique demandée
        if new_status:
            couturiere.is_accepted = True
            couturiere.user.is_active = True
        else:
            couturiere.is_accepted = False
            couturiere.user.is_active = False
            couturiere.refused_at = timezone.now() 
        
        # Sauvegarder les modifications
        couturiere.save()
        couturiere.user.save()
        
        
        Couturiere.objects.filter(
            is_accepted=False,
            refused_at__lt=timezone.now() - timedelta(days=30)
        ).delete()
        
        return Response({
            'message': 'Statut mis à jour avec succès',
            'is_accepted': couturiere.is_accepted,
            'is_active': couturiere.user.is_active
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': f'Erreur lors de la mise à jour: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        
        
        
        
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_couturiere_active_status(request, id):
    if request.user.role != 'admin':
        return Response(
            {"error": "Accès refusé. Seuls les administrateurs peuvent effectuer cette action."},
            status=status.HTTP_403_FORBIDDEN)
    try:
        
        # Récupérer la couturière
        couturiere = get_object_or_404(Couturiere, id=id)
        
        # Mettre à jour le statut is_active
        new_status = request.data.get('isactive')
        if new_status is not None:
            couturiere.user.is_active = bool(new_status)
            couturiere.user.save()
            
            return Response({
                "message": f"Statut actif mis à jour avec succès vers {new_status}",
                "is_active": couturiere.user.is_active
            }, status=200)
        else:
            return Response({"message": "Le champ 'isactive' est requis"}, status=400)
            
    except Exception as e:
        return Response({"message": f"Erreur: {str(e)}"}, status=500)
    
    
    
    
    
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def get_info_model_couturiere_waiting(request):
    if request.user.role != 'admin':
        return Response(
            {"error": "Accès refusé. Seuls les administrateurs peuvent effectuer cette action."},
            status=status.HTTP_403_FORBIDDEN)
   
    try:
        # Récupérer tous les modèles avec state='waiting' et owner non null
        fashion_models = FashionModel.objects.filter(
            state='waiting',
            owner__isnull=False,  # Vérifie que owner n'est pas null
            owner__role='couturiere'  # Vérifie que l'owner est une couturière
        ).select_related('owner').prefetch_related(
            'images',
            'variants'
        )
        
        # Préparer la liste des modèles
        models_data = []
        
        for model in fashion_models:
            try:
                # Récupérer les informations de la couturière
                couturiere_info = {}
                try:
                    couturiere = Couturiere.objects.get(user=model.owner)
                    couturiere_info = {
                        'full_name': model.owner.full_name,
                        'address': couturiere.address,
                        'phone_number': couturiere.phone_number
                    }
                except Couturiere.DoesNotExist:
                    couturiere_info = {
                        'full_name': model.owner.full_name if model.owner else 'N/A',
                        'address': 'Non disponible',
                        'phone_number': 'Non disponible'
                    }
                
                # Récupérer les images avec URL complète
                images_data = []
                for image in model.images.all():
                    if image.image:
                        # Construire l'URL complète
                        image_url = request.build_absolute_uri(image.image.url)
                    else:
                        image_url = None
                    
                    images_data.append({
                        'image_url': image_url
                    })
                
                # Récupérer les variants
                variants_data = []
                for variant in model.variants.all():
                    variants_data.append({
                        'size': variant.size,
                        'color': variant.color,
                        'quantity': variant.quantity
                    })
                
                # Construire l'objet modèle
                model_data = {
                    'id': model.id,
                    'description':model.description,
                    'namemodel': model.name,
                    'codemodel': model.code,
                    'price_per_piece_for_client': str(model.price_per_piece_for_client),
                    'statemodel': model.state,
                    'imagesmodel': images_data,
                    'variants': variants_data,
                    'couturiere_info': couturiere_info,
                }
                
                models_data.append(model_data)
                
            except Exception as e:
                # Continuer avec les autres modèles même si un échoue
                print(f"Erreur avec le modèle {model.id}: {str(e)}")
                continue
        
        return Response({
            'success': True,
            'count': len(models_data),
            'models': models_data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
        
        
        

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_fashion_model(request):
    # Vérifier que l'utilisateur a les permissions nécessaires
    if request.user.role != 'admin':  # Adaptez selon votre système de permissions
        return Response(
            {'error': 'Permission denied. Only admins can accept models.'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    # Récupérer le code du modèle depuis les paramètres de requête
    model_code = request.data.get('code')
    if not model_code:
        return Response(
            {'error': 'Model code is required.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Récupérer le modèle
    fashion_model = get_object_or_404(FashionModel, code=model_code)
    
    # Vérifier que le modèle est en état "waiting"
    if fashion_model.state != 'waiting':
        return Response(
            {'error': f'Model is not in waiting state. Current state: {fashion_model.state}'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Vérifier les champs obligatoires
    required_fields = ['price_per_piece_for_client', 'description']
    for field in required_fields:
        if field not in request.data:
            return Response(
                {'error': f'{field} is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    try:
        with transaction.atomic():
            # Mettre à jour l'état du modèle
            fashion_model.state = 'accepted'
            
            # Mettre à jour les champs obligatoires
            fashion_model.price_per_piece_for_client = request.data['price_per_piece_for_client']
            fashion_model.description = request.data['description']
            
            # Mettre à jour les champs facultatifs s'ils sont fournis
            if 'price_per_piece_for_dropshipper' in request.data:
                fashion_model.price_per_piece_for_dropshipper = request.data['price_per_piece_for_dropshipper']
            
            if 'arabic_name' in request.data:
                fashion_model.name = request.data['arabic_name']
            
            
            if 'min_quantity_for_dropshipper' in request.data:
                fashion_model.min_pieces_for_dropshipper = request.data['min_quantity_for_dropshipper']
            
            # Gérer les variantes si fournies
            if 'variants' in request.data:
                variants_data = request.data['variants']
                
                # Si c'est une chaîne JSON, la parser
                if isinstance(variants_data, str):
                    try:
                        variants_data = json.loads(variants_data)
                    except json.JSONDecodeError:
                        return Response(
                            {'error': 'Invalid JSON format for variants.'},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                
                # Supprimer toutes les variantes existantes pour ce modèle
                existing_variants = fashion_model.variants.all()
                for variant in existing_variants:
                    variant.delete()
                
                # Créer les nouvelles variantes
                for variant_data in variants_data:
                    size = variant_data.get('size')
                    color = variant_data.get('color')
                    quantity = variant_data.get('quantity')
                    
                    # Créer une nouvelle variante
                    new_variant = StockVariantForFashionModels.objects.create(
                        fashion_model=fashion_model,
                        size=size,
                        color=color,
                        quantity=quantity
                    )
            
            # Gérer les images supplémentaires
            existing_images = fashion_model.images.all()
            for image in existing_images:
                # Supprime le fichier image du stockage
                image.image.delete(save=False)
                # Supprime l'entrée de la base de données
                image.delete()
            
            # Ajouter les nouvelles images si elles sont fournies
            if 'images' in request.FILES:
                images = request.FILES.getlist('images')
                for image_file in images:
                    ModelImage.objects.create(
                        fashion_model=fashion_model,
                        image=image_file
                    )
            
            # Sauvegarder le modèle
            fashion_model.save()
            
            return Response(
                {
                    'message': 'Model accepted and updated successfully.',
                    'model_code': fashion_model.code,
                    'state': fashion_model.state
                },
                status=status.HTTP_200_OK
            )
    
    except ValidationError as e:
        return Response(
            {'error': f'Validation error: {str(e)}'},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {'error': f'An error occurred: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        
        
        
        
        
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def refuse_model_couturiere(request, model_code):
    if request.user.role != 'admin':  # Adaptez selon votre système de permissions
        return Response(
            {'error': 'Permission denied. Only admins can accept models.'},
            status=status.HTTP_403_FORBIDDEN
        )
    try:
        # Récupérer le modèle par son code
        fashion_model = get_object_or_404(FashionModel, code=model_code)
        
        # Vérifier si le modèle est dans l'état 'waiting'
        if fashion_model.state != 'waiting':
            return Response(
                {'error': 'Seuls les modèles avec state=waiting peuvent être annulés'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Mettre à jour l'état vers 'cancelled'
        fashion_model.state = 'cancelled'
        fashion_model.completed_at=timezone.now() 
        fashion_model.save()
        
        return Response(
            {
                'message': 'Modèle annulé avec succès',
                'model_code': fashion_model.code,
                'new_state': fashion_model.state
            },
            status=status.HTTP_200_OK
        )
        
    except Exception as e:
        return Response(
            {'error': f'Erreur lors de l\'annulation: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        
        
        
        
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_new_model_by_admin(request):
    if request.user.role != 'admin':  
        return Response(
            {'error': 'Permission denied. Only admins can accept models.'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    # Calculer la date limite (aujourd'hui - 2 mois)
    two_months_ago = timezone.now() - timedelta(days=60)
    
    # Récupérer les modèles à supprimer
    old_models = FashionModel.objects.filter(
        completed_at__isnull=False,
        completed_at__lt=two_months_ago
    ).exclude(state='accepted')
    
    # Supprimer ces modèles (cela supprimera aussi les variantes et images liées)
    old_models.delete()
    
    try:
        print(request.POST)
        # Récupérer les données du formulaire
        name = request.POST.get('name')
        description = request.POST.get('description')
        type = request.POST.get('type')
        price_per_piece_for_client = request.POST.get('price_per_piece_for_client')
        
        # Paramètres facultatifs
        price_per_piece_for_dropshipper = request.POST.get('price_per_piece_for_dropshipper', 0)
        min_pieces_for_dropshipper = request.POST.get('min_pieces_for_dropshipper', 1)
        
        # Vérifier les champs obligatoires
        if not all([name, description, type, price_per_piece_for_client]):
            return Response(
                {'error': 'Tous les champs obligatoires doivent être remplis'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Récupérer et parser le champ variants comme JSON
        variants_json = request.POST.get('variants')
        if not variants_json:
            return Response(
                {'error': 'Le champ variants est obligatoire'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            variants_data = json.loads(variants_json)
        except json.JSONDecodeError:
            return Response(
                {'error': 'Le format des variantes est invalide (doit être un JSON)'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Vérifier qu'il y a au moins une variante
        if not variants_data or not isinstance(variants_data, list):
            return Response(
                {'error': 'Au moins une variante est obligatoire'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # CORRECTION : Créer d'abord le modèle FashionModel
        fashion_model = FashionModel.objects.create(
            owner=None,
            name=name,
            type=type,
            price_per_piece_for_client=price_per_piece_for_client,
            price_per_piece_for_dropshipper=price_per_piece_for_dropshipper,
            description=description,
            min_pieces_for_dropshipper=min_pieces_for_dropshipper,
            state='accepted'
        )
        
        created_variants = []
        for variant in variants_data:
            size = variant.get('size')
            color = variant.get('color')
            quantity = variant.get('quantity')
            
            if not all([size, color, quantity]):
                # Nettoyer le modèle créé en cas d'erreur
                fashion_model.delete()
                return Response(
                    {'error': 'Chaque variante doit avoir size, color et quantity'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # CORRECTION : Créer la variante avec la référence au modèle
            stock_variant = StockVariantForFashionModels.objects.create(
                fashion_model=fashion_model,  # Ajouter cette ligne
                size=size,
                color=color,
                quantity=quantity
            )
            created_variants.append(stock_variant)
        
        # Traiter les images
        images = request.FILES.getlist('images')
        for image_file in images:
            ModelImage.objects.create(
                fashion_model=fashion_model,
                image=image_file
            )
        
        return Response(
            {
                'message': 'Modèle ajouté avec succès',
                'model_id': fashion_model.id,
                'code': fashion_model.code,
                'total_variants': len(created_variants),
                'total_images': len(images)
            },
            status=status.HTTP_201_CREATED
        )
        
    except Exception as e:
        return Response(
            {'error': f'Erreur lors de la création du modèle: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        
        
        
        
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_fashion_model(request, model_code):
    if request.user.role != 'admin':  
        return Response(
            {'error': 'Permission denied. Only admins can accept models.'},
            status=status.HTTP_403_FORBIDDEN
        )
    try:
        # Récupérer le modèle par son code
        fashion_model = get_object_or_404(FashionModel, code=model_code)
        # Vérifier s'il existe des commandes liées à ce modèle
        related_orders = Order.objects.filter(fashion_model=fashion_model)
        
        if related_orders.exists():
            # S'il y a des commandes, on change seulement l'état
            fashion_model.state = 'notvisible'
            fashion_model.completed_at=timezone.now() 
            fashion_model.save()
            
            return Response(
                {
                    "message": "Le modèle a été masqué (état changé à 'notvisible') car des commandes y sont associées",
                    "model_code": model_code,
                    "state": fashion_model.state,
                    "related_orders_count": related_orders.count()
                },
                status=status.HTTP_200_OK
            )
        else:
            # Si aucune commande, on supprime complètement
            fashion_model.delete()
            
            return Response(
                {
                    "message": "Le modèle a été supprimé définitivement car aucune commande n'y est associée",
                    "model_code": model_code,
                    "deleted": True
                },
                status=status.HTTP_200_OK
            )
            
    except FashionModel.DoesNotExist:
        return Response(
            {"error": f"Modèle avec le code {model_code} non trouvé"},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {"error": f"Erreur lors du traitement: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        
        
        
        
        
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_commande_fassou(request):
    try:
        # Vérifier que l'utilisateur est un admin
        if request.user.role != 'admin':
            return Response(
                {'error': 'Seuls les administrateurs peuvent créer des commandes Fassou'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Récupérer les données du body
        data = request.data
        
        # Valider les champs obligatoires
        required_fields = ['nameorder', 'modeltype', 'deadline', 'initialprice', 'description', 'variants']
        for field in required_fields:
            if field not in data:
                return Response(
                    {'error': f'Le champ {field} est obligatoire'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Parser les variantes
        variants_json = data.get('variants', '[]')
        try:
            variants_data = json.loads(variants_json)
        except json.JSONDecodeError:
            return Response(
                {'error': 'Format JSON invalide pour les variantes'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Vérifier qu'il y a au moins une variante
        if not variants_data or not isinstance(variants_data, list):
            return Response(
                {'error': 'Au moins une variante est obligatoire'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Créer la commande Fassou
        commande = CustomOrder.objects.create(
            user=request.user,
            nameorder=data['nameorder'],
            model_type=data['modeltype'],
            deadline=data['deadline'],
            description=data['description'],
            initial_price=data['initialprice'],
            command_type='fassou',
            state='pending',
            assigned_couturiere=None,
            wilaya=None,
            exactaddress=None
        )
        
        # Créer et associer les variantes de stock
        for variant_data in variants_data:
            # Chercher si une variante existe déjà avec les mêmes caractéristiques
            variant = StockVariantForCommands.objects.filter(
                size=variant_data['size'],
                color=variant_data['color'],
                quantity=variant_data['quantity']
            ).first()
            
            # Si la variante n'existe pas, la créer
            if not variant:
                variant = StockVariantForCommands.objects.create(
                    size=variant_data['size'],
                    color=variant_data['color'],
                    quantity=variant_data['quantity']
                )
            
            # Associer la variante à la commande
            commande.command_details.add(variant)
        
        # Traiter les images/PDF (sans les champs size, color, quantity)
        if 'images' in request.FILES:
            for image_file in request.FILES.getlist('images'):
                CustomOrderImage.objects.create(
                    fashion_model=commande,
                    image=image_file
                )
        
        return Response(
            {
                'message': 'Commande Fassou créée avec succès',
                'codeorder': commande.codeorder,
                'commande_id': commande.id,
                'total_images': len(request.FILES.getlist('images')) if 'images' in request.FILES else 0
            },
            status=status.HTTP_201_CREATED
        )
        
    except Exception as e:
        return Response(
            {'error': f'Erreur lors de la création: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        
        
        
        
        

        
        
        
        
        
        
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getInfoCommandeFassou(request):
    try:
        # Précharger les relations pour optimiser les requêtes
        orders = CustomOrder.objects.filter(
            command_type='fassou'
        ).prefetch_related(
            Prefetch('command_details', queryset=StockVariantForCommands.objects.all()),
            Prefetch('custom_images', queryset=CustomOrderImage.objects.all()),
            Prefetch('assigned_couturiere', queryset=User.objects.prefetch_related('couturiere'))
        )
        
        orders_data = []
        
        for order in orders:
            # Récupérer les variantes de la commande
            variants_data = []
            for variant in order.command_details.all():
                variants_data.append({
                    'size': variant.size,
                    'color': variant.color,
                    'quantity': variant.quantity
                })
            
            # Récupérer les images du modèle
            images_data = []
            for image in order.custom_images.all():
                images_data.append({
                    'id': image.id,
                    'image_url': request.build_absolute_uri(image.image.url) if image.image else None
                })
            
            # Construire les données de base de la commande
            order_data = {
                'nameorder': order.nameorder,
                'codeorder': order.codeorder,
                'deadline': order.deadline,
                'variants': variants_data,
                'command_type': order.command_type,
                'model_type': order.model_type,
                'state': order.state,
                'initial_price': float(order.initial_price) if order.initial_price else None,
                'description': order.description,
                'created_at': order.created_at,
                'updated_at': order.updated_at,
                'images': images_data,
            }
            print()
            # Ajouter les informations de la couturière si la commande est assignée
            if (order.state in ['inprogress', 'done', 'cancelled'] and 
                order.assigned_couturiere and 
                order.assigned_couturiere.is_active):
                
                # Utiliser la relation préchargée au lieu de faire une nouvelle requête
                if hasattr(order.assigned_couturiere, 'couturiere'):
                    couturiere_profile = order.assigned_couturiere.couturiere
                    if couturiere_profile.is_accepted:
                        order_data['couturiere_info'] = {
                            'full_name': order.assigned_couturiere.full_name,
                            'email': order.assigned_couturiere.email,
                            'phone_number': couturiere_profile.phone_number,
                            'address': couturiere_profile.address,
                        }
                    else:
                        order_data['couturiere_info'] = None
                else:
                    order_data['couturiere_info'] = None
            else:
                order_data['couturiere_info'] = None
            
            orders_data.append(order_data)
        
        return Response({
            'success': True,
            'count': len(orders_data),
            'orders': orders_data
        })
        
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=500)
        
        
        
        
        
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def make_fassou_command_completed(request, codeorder):
    try:
        # Récupérer la commande par son code
        order = get_object_or_404(CustomOrder, codeorder=codeorder, command_type='fassou')
        
        # Vérifications supplémentaires
        if order.state == 'done':
            return Response({
                'success': False,
                'error': 'Cette commande est déjà terminée'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        
        # Vérifier que la commande est assignée à une couturière
        if not order.assigned_couturiere:
            return Response({
                'success': False,
                'error': 'Cette commande n\'est pas assignée à une couturière'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Changer l'état de la commande
        order.state = 'done'
        order.completed_at = timezone.now()  

        order.save()
        
        
        two_months_ago = timezone.now() - timezone.timedelta(days=60)
        old_orders = CustomOrder.objects.filter(
        command_type='fassou',
        state__in=['done', 'cancelled'],
        completed_at__lt=two_months_ago
         )
        old_orders.delete()
        
        # Préparer les données de réponse
        order_data = {
            'codeorder': order.codeorder,
            'nameorder': order.nameorder,
            'state': order.state,
            'updated_at': order.updated_at,
            'couturiere_assigned': order.assigned_couturiere.full_name if order.assigned_couturiere else None
        }
        
        return Response({
            'success': True,
            'message': 'Commande marquée comme terminée avec succès',
            'order': order_data
        })
        
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
        
        
        
        
        
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def make_fassou_command_refused(request, codeorder):
    try:
        # Récupérer la commande par son code
        order = get_object_or_404(CustomOrder, codeorder=codeorder, command_type='fassou')
        
        # Vérifications supplémentaires
        if order.state == 'cancelled':
            return Response({
                'success': False,
                'error': 'Cette commande est déjà cancelled'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        
        # Vérifier que la commande est assignée à une couturière
        if not order.assigned_couturiere:
            return Response({
                'success': False,
                'error': 'Cette commande n\'est pas assignée à une couturière'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Changer l'état de la commande
        order.state = 'cancelled'
        order.completed_at=timezone.now()
        order.save()
        
        # Préparer les données de réponse
        order_data = {
            'codeorder': order.codeorder,
            'nameorder': order.nameorder,
            'state': order.state,
            'updated_at': order.updated_at,
            'couturiere_assigned': order.assigned_couturiere.full_name if order.assigned_couturiere else None
        }
        
        return Response({
            'success': True,
            'message': 'Commande marquée comme refussée avec succès',
            'order': order_data
        })
        
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
        
        
        
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_total_benefit_from_saling_products_personalized_standard_in_month(request):
    # Vérifier que l'utilisateur est un admin
    if request.user.role != 'admin':
        return Response({"error": "Accès non autorisé"}, status=403)
    
    # Calculer la date de début (30 jours avant aujourd'hui)
    end_date = timezone.now()
    start_date = end_date - timedelta(days=30)
    
    # Initialiser le dictionnaire pour stocker les bénéfices par date
    daily_benefits = {}
    
    # Récupérer toutes les dates dans la plage
    current_date = start_date
    while current_date <= end_date:
        date_key = current_date.date().isoformat()
        daily_benefits[date_key] = {
            'custom_orders_benefit': 0,
            'standard_orders_benefit': 0,
            'total_benefit': 0
        }
        current_date += timedelta(days=1)
    
    # PARTIE 1: Commandes personnalisées
    custom_orders = CustomOrder.objects.filter(
        state='done',
        completed_at__date__gte=start_date.date(),
        completed_at__date__lte=end_date.date(),
        command_type='personalized'
    )
    
    for order in custom_orders:
        order_date = order.completed_at.date().isoformat()
        
        # Calculer le bénéfice pour cette commande
        total_quantity = 0
        for variant in order.command_details.all():
            total_quantity += variant.quantity
        
        order_benefit = order.initial_price * total_quantity
        
        # Ajouter au bénéfice quotidien
        if order_date in daily_benefits:
            daily_benefits[order_date]['custom_orders_benefit'] += order_benefit
            daily_benefits[order_date]['total_benefit'] += order_benefit
    
    # PARTIE 2: Commandes standard
    standard_orders = Order.objects.filter(
        state='done',
        completed_at__date__gte=start_date.date(),
        completed_at__date__lte=end_date.date()
    )
    
    for order in standard_orders:
        order_date = order.completed_at.date().isoformat()
        
        # Calculer la quantité totale de la commande
        total_quantity = 0
        for variant in order.standard_command_details.all():
            total_quantity += variant.quantity
        
        # Calculer le prix unitaire après réduction si promo code existe
        if order.dropshipper_client:
          base_price = order.fashion_model.price_per_piece_for_dropshipper
        else:
          base_price = order.fashion_model.price_per_piece_for_client
        
        if order.promo_code:
            discount_percentage = (order.promo_code.discount_percentage + order.promo_code.profit_percentage )/ 100
            unit_price = base_price * (1 - discount_percentage)
        else:
            unit_price = base_price
        
        # Calculer le bénéfice pour cette commande
        order_benefit = unit_price * total_quantity
        
        # Ajouter au bénéfice quotidien
        if order_date in daily_benefits:
            daily_benefits[order_date]['standard_orders_benefit'] += order_benefit
            daily_benefits[order_date]['total_benefit'] += order_benefit
    
    # Préparer la réponse
    response_data = {
        'period': {
            'start_date': start_date.date().isoformat(),
            'end_date': end_date.date().isoformat()
        },
        'daily_benefits': daily_benefits,
        'total_custom_benefit': sum(day['custom_orders_benefit'] for day in daily_benefits.values()),
        'total_standard_benefit': sum(day['standard_orders_benefit'] for day in daily_benefits.values()),
        'grand_total': sum(day['total_benefit'] for day in daily_benefits.values())
    }
    
    return Response(response_data)







@api_view(['GET'])
def verify_if_we_are_able_to_modify_model(request, model_code):
    try:
        # Trouver le modèle par son code UUID
        fashion_model = FashionModel.objects.get(code=model_code)
    except FashionModel.DoesNotExist:
        return Response(
            {"error": "Modèle non trouvé"}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Vérifier si le modèle a des commandes
    orders = Order.objects.filter(fashion_model=fashion_model)
    
    if not orders.exists():
        # Aucune commande → "yes"
        return Response({"response": "yes,make changes"})
    
    # Vérifier si toutes les commandes sont terminées (done) ou refusées (refused)
    # On exclut les commandes qui ne sont PAS dans l'état 'done' ou 'refused'
    pending_orders = orders.exclude(state__in=['done', 'refused'])
    
    if not pending_orders.exists():
        # Toutes les commandes sont soit 'done' soit 'refused' → "yes"
        return Response({"response": "yes,make changes"})
    else:
        # Il y a des commandes en attente ou dans d'autres états → "no"
        return Response({"response": "no,you can't make changes"})
    
    
    
    
    
    
    
    
    

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def change_model_from_not_visible_to_accepted(request, model_code):
    if request.user.role != 'admin':
        return Response({"error": "Accès non autorisé"}, status=403)
    
    try:
        # Récupérer le modèle
        fashion_model = get_object_or_404(FashionModel, code=model_code)
        
        # Vérifier si le modèle est déjà dans un état autre que "notvisible"
        if fashion_model.state != 'notvisible':
            return JsonResponse({
                'status': 'no_change',
                'message': f'Le modèle {model_code} n\'est pas dans l\'état "notvisible". Aucun changement effectué.'
            })
        
        # Vérifier s'il existe des commandes en attente pour ce modèle
        waiting_orders = Order.objects.filter(
            fashion_model=fashion_model,
            state='waiting'
        )
        
        # Cas 1: Aucune commande en attente
        if not waiting_orders.exists():
            # Vérifier s'il y a au moins une variante avec quantité > 0
            has_available_variants = StockVariantForFashionModels.objects.filter(
                fashion_model=fashion_model,
                quantity__gt=0
            ).exists()
            
            if has_available_variants:
                fashion_model.state = 'accepted'
                fashion_model.save()
                return JsonResponse({
                    'status': 'success',
                    'message': f'Le modèle {model_code} a été changé à "accepted" car il a des variantes disponibles et aucune commande en attente.'
                })
            else:
                return JsonResponse({
                    'status': 'no_change',
                    'message': f'Le modèle {model_code} n\'a pas de variantes disponibles. Aucun changement effectué.'
                })
        
        # Cas 2: Il y a des commandes en attente
        else:
            # Récupérer toutes les variantes du modèle avec leurs quantités
            model_variants = StockVariantForFashionModels.objects.filter(
                fashion_model=fashion_model
            )
            
            # Créer un dictionnaire pour suivre les quantités disponibles par variante
            available_quantities = {}
            for variant in model_variants:
                key = (variant.size, variant.color)
                available_quantities[key] = variant.quantity
            
            # Calculer la demande totale pour chaque variante à partir des commandes en attente
            demanded_quantities = {}
            for order in waiting_orders:
                # Récupérer les détails de la commande (variantes commandées)
                command_variants = order.standard_command_details.all()
                
                for variant in command_variants:
                    key = (variant.size, variant.color)
                    if key in demanded_quantities:
                        demanded_quantities[key] += variant.quantity
                    else:
                        demanded_quantities[key] = variant.quantity
            
            # Vérifier si le stock peut satisfaire toutes les commandes en attente
            can_fulfill_all_orders = True
            for key, demanded_qty in demanded_quantities.items():
                available_qty = available_quantities.get(key, 0)
                if available_qty < demanded_qty:
                    can_fulfill_all_orders = False
                    break
            
            # Vérifier s'il reste des variantes disponibles après satisfaction des commandes
            has_remaining_variants = False
            if can_fulfill_all_orders:
                # Calculer les quantités restantes après satisfaction des commandes
                for key, available_qty in available_quantities.items():
                    demanded_qty = demanded_quantities.get(key, 0)
                    remaining_qty = available_qty - demanded_qty
                    
                    # Vérifier s'il reste des quantités disponibles
                    if remaining_qty > 0:
                        has_remaining_variants = True
                        break
                
                # Vérifier s'il y a des variantes qui ne sont pas demandées
                if not has_remaining_variants:
                    for key, available_qty in available_quantities.items():
                        if key not in demanded_quantities and available_qty > 0:
                            has_remaining_variants = True
                            break
            
            # Décision finale
            if can_fulfill_all_orders and has_remaining_variants:
                fashion_model.state = 'accepted'
                fashion_model.completed_at=None
                fashion_model.save()
                return JsonResponse({
                    'status': 'success',
                    'message': f'Le modèle {model_code} a été changé à "accepted" car il peut satisfaire toutes les commandes en attente et il reste des variantes disponibles.'
                })
            else:
                return JsonResponse({
                    'status': 'no_change',
                    'message': f'Le modèle {model_code} ne peut pas être rendu visible car il ne peut pas satisfaire toutes les commandes en attente ou il ne reste pas de variantes disponibles.'
                })
    
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Une erreur s\'est produite: {str(e)}'
        }, status=500)