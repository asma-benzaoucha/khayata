from django.shortcuts import render
import random
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Count, Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from django.utils import timezone
from django.db import transaction
import json
from rest_framework import viewsets



from Backendkadi.models.commandes import  CustomOrder 
from Backendkadi.models.user import  User ,Client,Dropshipper,DropshipperClients
from Backendkadi.models.commandes import Order
from Backendkadi.models.modeles import  FashionModel
from Backendkadi.models.commandes import CustomOrder,Order
from Backendkadi.models.livraison import WilayaDelivery
from Backendkadi.models.promo import PromoCode
from Backendkadi.models.stock import StockVariantForCommands,StockVariantForFashionModels

from Backendkadi.models.socialAccountsLinkgroups import SocialAccountsLinkGroup
from Backendkadi.utils import send_verification_email



from .serializers import FashionModelSerializer
from .serializers import FashionModelSerializer2
from .serializers import CustomOrderSerializer, OrderSerializer
from .serializers import ClientSignupSerializer
from .serializers import WilayaDeliverySerializer
from .serializers import CustomOrderSerializer2
from .serializers import SocialAccountsLinkGroupSerializer








class TopSellingFashionModelsView(generics.ListAPIView):
    serializer_class = FashionModelSerializer

    def get_queryset(self):
        # Récupérer les modèles avec des commandes 'done' et les trier par nombre de ventes
        top_models = FashionModel.objects.filter(
            orders__state='done',
            state='accepted'  # Seulement les modèles acceptés
        ).annotate(
            sales_count=Count('orders', filter=Q(orders__state='done'))
        ).order_by('-sales_count')[:3]  # Les 3 plus vendus
        
        # Créer un dictionnaire pour suivre les types de sélection
        selection_types = {}
        for model in top_models:
            selection_types[model.id] = 'top'
        
        # Si on a moins de 3 modèles vendus, compléter avec des modèles aléatoires
        if top_models.count() < 3:
            # Récupérer les IDs des modèles déjà sélectionnés
            existing_ids = list(top_models.values_list('id', flat=True))
            
            # Récupérer des modèles aléatoires qui ne sont pas déjà dans la liste
            # et qui sont acceptés
            remaining_models = FashionModel.objects.filter(
                state='accepted'
            ).exclude(id__in=existing_ids)
            
            # Calculer combien de modèles supplémentaires nous avons besoin
            needed_count = 3 - top_models.count()
            
            # Si on a assez de modèles, en sélectionner aléatoirement
            if remaining_models.count() >= needed_count:
                random_models = random.sample(list(remaining_models), needed_count)
                # Marquer ces modèles comme "random"
                for model in random_models:
                    selection_types[model.id] = 'random'
                # Combiner les deux listes
                top_models = list(top_models) + random_models
            else:
                # S'il n'y a pas assez de modèles, prendre tous ceux disponibles
                for model in remaining_models:
                    selection_types[model.id] = 'random'
                top_models = list(top_models) + list(remaining_models)
        
        # Stocker les types de sélection dans l'instance de vue pour utilisation dans get_serializer_context
        self.selection_types = selection_types
        
        return top_models

    def get_serializer_context(self):
        # Passer le contexte au serializer
        context = super().get_serializer_context()
        context['selection_types'] = getattr(self, 'selection_types', {})
        return context




@api_view(['POST'])
@permission_classes([AllowAny])
def client_signup(request):
    serializer = ClientSignupSerializer(data=request.data)
    
    if serializer.is_valid():
        client = serializer.save()
        
        # Envoyer l'email de vérification
        send_verification_email(client.user)
        
        return Response({
            'message': 'Compte créé avec succès. Veuillez vérifier votre email pour activer votre compte.',
            'user_id': client.user.id
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)







class FashionModelListView(generics.ListAPIView):
  
  serializer_class = FashionModelSerializer2
  permission_classes = [IsAuthenticated] 
  
    
  def get_queryset(self):
    user = self.request.user
    if user.role != 'dropshipper' and user.role != 'client' and user.role != 'admin':
        return Response({"error": "Accès non autorisé"}, status=403)
    
    queryset = FashionModel.objects.filter(state='accepted')
    
    
    print(f"User: {user}, Authenticated: {user.is_authenticated}, Role: {getattr(user, 'role', 'None')}")
    
    if user.is_authenticated and user.role == 'dropshipper':
        print("Applying dropshipper filter: price > 0")
        queryset = queryset.filter(price_per_piece_for_dropshipper__gt=0)
        print(f"Filtered queryset count after price filter: {queryset.count()}")
        
        # Filtrer les modèles où min_pieces_for_dropshipper <= quantité totale des variantes
        filtered_models = []
        for model in queryset:
            total_quantity = model.total_pieces()  # Utilise la méthode existante du modèle
            if model.min_pieces_for_dropshipper <= total_quantity:
                filtered_models.append(model.id)
        
        # Refiltrer le queryset avec les IDs valides
        queryset = queryset.filter(id__in=filtered_models)
        print(f"Filtered queryset count after quantity check: {queryset.count()}")
    
    return queryset
    
    
    
#get all women models accepted from the store 
class FashionModelFemmeListView(generics.ListAPIView):
  serializer_class = FashionModelSerializer2
  permission_classes = [IsAuthenticated] 
    
    
  def get_queryset(self):
    user = self.request.user
    if user.role != 'dropshipper' and user.role != 'client':
        return Response({"error": "Accès non autorisé"}, status=403)
    
    queryset = FashionModel.objects.filter(type='femme', state='accepted')
    
    
    print(f"User: {user}, Authenticated: {user.is_authenticated}, Role: {getattr(user, 'role', 'None')}")
    
    if user.is_authenticated and user.role == 'dropshipper':
        print("Applying dropshipper filter: price > 0")
        queryset = queryset.filter(price_per_piece_for_dropshipper__gt=0)
        print(f"Filtered queryset count after price filter: {queryset.count()}")
        
        # Filtrer les modèles où min_pieces_for_dropshipper <= quantité totale des variantes
        filtered_models = []
        for model in queryset:
            total_quantity = model.total_pieces()  # Utilise la méthode existante du modèle
            if model.min_pieces_for_dropshipper <= total_quantity:
                filtered_models.append(model.id)
        
        # Refiltrer le queryset avec les IDs valides
        queryset = queryset.filter(id__in=filtered_models)
        print(f"Filtered queryset count after quantity check: {queryset.count()}")
    
    return queryset
    
   

#get all homme models accepted from the store 
class FashionModelHommeListView(generics.ListAPIView):
  serializer_class = FashionModelSerializer2
  permission_classes = [IsAuthenticated]
    
    
  def get_queryset(self):
    user = self.request.user
    if user.role != 'dropshipper' and user.role != 'client':
        return Response({"error": "Accès non autorisé"}, status=403)
    
    queryset = FashionModel.objects.filter(type='homme', state='accepted')
    
    
    print(f"User: {user}, Authenticated: {user.is_authenticated}, Role: {getattr(user, 'role', 'None')}")
    
    if user.is_authenticated and user.role == 'dropshipper':
        print("Applying dropshipper filter: price > 0")
        queryset = queryset.filter(price_per_piece_for_dropshipper__gt=0)
        print(f"Filtered queryset count after price filter: {queryset.count()}")
        
        # Filtrer les modèles où min_pieces_for_dropshipper <= quantité totale des variantes
        filtered_models = []
        for model in queryset:
            total_quantity = model.total_pieces()  # Utilise la méthode existante du modèle
            if model.min_pieces_for_dropshipper <= total_quantity:
                filtered_models.append(model.id)
        
        # Refiltrer le queryset avec les IDs valides
        queryset = queryset.filter(id__in=filtered_models)
        print(f"Filtered queryset count after quantity check: {queryset.count()}")
    
    return queryset
    

#get all enfant models accepted from the store 
class FashionModelEnfantListView(generics.ListAPIView):
  serializer_class = FashionModelSerializer2
  permission_classes = [IsAuthenticated]
    
    
  def get_queryset(self):
    user = self.request.user
    if user.role != 'dropshipper' and user.role != 'client':
        return Response({"error": "Accès non autorisé"}, status=403)
    
    queryset = FashionModel.objects.filter(type='enfant', state='accepted')
    
    
    print(f"User: {user}, Authenticated: {user.is_authenticated}, Role: {getattr(user, 'role', 'None')}")
    
    if user.is_authenticated and user.role == 'dropshipper':
        print("Applying dropshipper filter: price > 0")
        queryset = queryset.filter(price_per_piece_for_dropshipper__gt=0)
        print(f"Filtered queryset count after price filter: {queryset.count()}")
        
        # Filtrer les modèles où min_pieces_for_dropshipper <= quantité totale des variantes
        filtered_models = []
        for model in queryset:
            total_quantity = model.total_pieces()  # Utilise la méthode existante du modèle
            if model.min_pieces_for_dropshipper <= total_quantity:
                filtered_models.append(model.id)
        
        # Refiltrer le queryset avec les IDs valides
        queryset = queryset.filter(id__in=filtered_models)
        print(f"Filtered queryset count after quantity check: {queryset.count()}")
    
    return queryset
    
    





# Dans views.py

#get all orders et custom order for a  client (page talabiyati)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_client_orders(request):
    # Récupérer l'utilisateur connecté depuis le token JWT
    client = request.user
    
    # Vérifier que l'utilisateur est bien un client
    if client.role != 'client' and client.role != 'dropshipper':
        return Response(
            {'error': 'Accès non autorisé. Seuls les clients peuvent accéder à leurs commandes.'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    # Récupérer les commandes standard du client
    standard_orders = Order.objects.filter(user=client).select_related(
        'fashion_model', 'promo_code', 'wilaya'
    ).prefetch_related(
        'standard_command_details', 'fashion_model__images'
    )
    
    # Récupérer les commandes personnalisées du client
    custom_orders = CustomOrder.objects.filter(
        user=client, command_type='personalized'
    ).select_related('wilaya').prefetch_related(
        'command_details', 'custom_images'
    )
    
    standard_serializer = OrderSerializer(standard_orders, many=True)
    custom_serializer = CustomOrderSerializer(custom_orders, many=True)
    
    # Combiner les résultats
    response_data = {
        'standard_orders': standard_serializer.data,
        'custom_orders': custom_serializer.data
    }
    
    return Response(response_data, status=status.HTTP_200_OK)












@api_view(['GET'])
def delivery_price_api(request):
    wilaya_name = request.GET.get('wilaya_name')
    
    if not wilaya_name:
        return Response(
            {'error': 'Le paramètre wilaya_name est requis'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        wilaya = WilayaDelivery.objects.get(wilaya_name__iexact=wilaya_name)
        serializer = WilayaDeliverySerializer(wilaya)
        return Response(serializer.data)
    
    except WilayaDelivery.DoesNotExist:
        return Response(
            {'error': f'Wilaya "{wilaya_name}" non trouvée'},
            status=status.HTTP_404_NOT_FOUND
        )
        






#verify if a code promo is valid ? 
@api_view(['GET'])
def validate_promo_code(request, code, modelCode):
    # Vérifier d'abord si le modèle existe
    try:
        fashion_model = FashionModel.objects.get(code=modelCode)
    except FashionModel.DoesNotExist:
        return Response({
            'valid': False,
            'message': 'المنتج غير موجود',
            'discount_percentage': 0
        }, status=status.HTTP_200_OK)
    
    # Vérifier ensuite si le code promo existe
    try:
        promo_code = PromoCode.objects.get(code=code)
    except PromoCode.DoesNotExist:
        return Response({
            'valid': False,
            'message': 'الكود الذي أدخلته غير صحيح',
            'discount_percentage': 0
        }, status=status.HTTP_200_OK)
    
    # Vérifier la validité temporelle
    if not promo_code.is_valid():
        return Response({
            'valid': False,
            'message': 'الكود منتهي الصلاحية و لم يعد فعال',
            'discount_percentage': 0
        }, status=status.HTTP_200_OK)
    
    # Vérifier l'association avec le modèle
    if not promo_code.models.filter(code=modelCode).exists():
        return Response({
            'valid': False,
            'message': 'هذا الكود غير صالح لهذا المنتج',
            'discount_percentage': 0
        }, status=status.HTTP_200_OK)
    
    # Tout est valide
    return Response({
        'valid': True,
        'discount_percentage': float(promo_code.discount_percentage),
        'code': promo_code.code,
        'message': 'Code promo valide'
    }, status=status.HTTP_200_OK)
        
        
        
        
        
     
     
     
     
        
#requete post pour faire une demande d'acheter un model de la part de client 
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@transaction.atomic
def create_order(request):
    
    try:
        # Récupérer les données du body
        data = request.data
        if request.user.role != 'client' and request.user.role != 'dropshipper':
            return Response(
                {"error": "Seuls les clients et dropshippers peuvent acheter un modèle"},
                status=status.HTTP_403_FORBIDDEN
            )
            
            
        if request.user.role == 'dropshipper':
            if not request.user.is_active:
                return Response(
                    {"error": "Ce dropshipper n'est pas actif"},
                    status=status.HTTP_403_FORBIDDEN
                )
            # Vérifier la présence du champ name_acheteur pour les dropshippers
            if 'name_acheteur' not in data:
                return Response(
                    {'error': 'Le champ name_acheteur est requis pour les dropshippers.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
                
            
        
        # Valider les données requises
        required_fields = ['phone_number', 'address', 'model_code', 'wilaya_name', 'variants']
        for field in required_fields:
            if field not in data:
                return Response(
                    {'error': f'Le champ {field} est requis.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Trouver le modèle de fashion
        try:
            fashion_model = FashionModel.objects.get(code=data['model_code'])
        except FashionModel.DoesNotExist:
            return Response(
                {'error': 'Modèle de fashion non trouvé.'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Trouver la wilaya
        try:
            wilaya = WilayaDelivery.objects.get(wilaya_name=data['wilaya_name'])
        except WilayaDelivery.DoesNotExist:
            return Response(
                {'error': 'Wilaya non trouvée.'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Traiter le code promo s'il est fourni
        promo_code_obj = None
        if 'promo_code' in data and data['promo_code']:
            try:
                promo_code_obj = PromoCode.objects.get(code=data['promo_code'])
                if not promo_code_obj.is_valid():
                    return Response(
                        {'error': 'Code promo expiré ou invalide.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            except PromoCode.DoesNotExist:
                return Response(
                    {'error': 'Code promo non trouvé.'},
                    status=status.HTTP_404_NOT_FOUND
                )
        
        
        
        dropshipper_client_obj = None
        if request.user.role == 'dropshipper' and request.user.is_active:
            try:
                dropshipper_profile = Dropshipper.objects.get(user=request.user)
                # Créer ou récupérer le client dropshipper
                dropshipper_client_obj, created = DropshipperClients.objects.get_or_create(
                    dropshipper=dropshipper_profile,
                    nom_client=data['name_acheteur']
                )
            except Dropshipper.DoesNotExist:
                return Response(
                    {'error': 'Profil dropshipper non trouvé.'},
                    status=status.HTTP_404_NOT_FOUND
                )
        # Créer la commande
        order = Order.objects.create(
            user=request.user,
            phone_number=data['phone_number'],
            address=data['address'],
            fashion_model=fashion_model,
            wilaya=wilaya,
            promo_code=promo_code_obj,
            state='pending',
            dropshipper_client=dropshipper_client_obj if request.user.role == 'dropshipper' else None

        )
        
        
        
       
        variants_data = data['variants']
        for variant_data in variants_data:
            size = variant_data.get('size')
            color = variant_data.get('color')
            quantity = int(variant_data.get('quantity'))
            
        
            stock_variant, created = StockVariantForCommands.objects.get_or_create(
                size=size,
                color=color,
                quantity=quantity
            )
            
            # Ajouter la variante à la commande
            order.standard_command_details.add(stock_variant)
            stock_variant.save()
        
        # Sauvegarder la commande
        order.save()
        
        
        return Response(
            {
                'message': 'Commande créée avec succès.',
                'order_id': order.id,
                'order_code': order.code_order
            },
            status=status.HTTP_201_CREATED
        )
    
    except Exception as e:
        return Response(
            {'error': f'Erreur lors de la création de la commande: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        
        
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_client_name(request):
    try:
        # Vérifier que l'utilisateur est un client
        # try:
        #     client = Client.objects.get(user=request.user)
        # except Client.DoesNotExist:
        #     return Response(
        #         {"error": "Seul un client peut modifier son nom."},
        #         status=status.HTTP_403_FORBIDDEN
        #     ) tous les utilisateurs peuvent changer leurs noms 
        
        # Vérifier et parser les données
        data = json.loads(request.body)
        new_full_name = data.get('full_name')
        
        if not new_full_name:
            return Response(
                {"error": "Le champ 'full_name' est requis."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Mettre à jour le nom de l'utilisateur
        user = request.user
        user.full_name = new_full_name
        user.save()
        
        return Response(
            {"message": "Nom mis à jour avec succès", "new_full_name": new_full_name},
            status=status.HTTP_200_OK
        )
            
    except json.JSONDecodeError:
        return Response(
            {"error": "Données JSON invalides."},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {"error": f"Erreur serveur: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        
        
        

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_special_command(request):
    # Vérifier que l'utilisateur est un client
    if request.user.role != 'client':
        return Response(
            {"error": "Seuls les clients peuvent créer des commandes personnalisées"},
            status=status.HTTP_403_FORBIDDEN
        )
    
    serializer = CustomOrderSerializer2(
        data=request.data,
        context={'request': request}
    )
    
    if serializer.is_valid():
        try:
            order = serializer.save()
            return Response(
                {
                    "message": "Commande personnalisée créée avec succès",
                    "order_id": order.id,
                    "total_quantity": order.total_requested_quantity()
                },
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {"error": f"Erreur lors de la création: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 





#get all social and group links 
class SocialLinksList(APIView):
    def get(self, request):
        social_links = SocialAccountsLinkGroup.objects.all()
        serializer = SocialAccountsLinkGroupSerializer(social_links, many=True)
        return Response(serializer.data)