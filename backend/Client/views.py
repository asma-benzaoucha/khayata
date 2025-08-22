from django.shortcuts import render
import random
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Count, Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny


from .serializers import FashionModelSerializer
from .serializers import FashionModelSerializer2
from .serializers import CustomOrderSerializer, OrderSerializer
from .serializers import ClientSignupSerializer
from .serializers import WilayaDeliverySerializer


from Backendkadi.models.commandes import  CustomOrder 
from Backendkadi.models.commandes import Order
from Backendkadi.models.modeles import  FashionModel
from Backendkadi.models.commandes import CustomOrder,Order
from Backendkadi.models.livraison import WilayaDelivery
from Backendkadi.utils import send_verification_email
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
                # Combiner les deux listes
                top_models = list(top_models) + random_models
            else:
                # S'il n'y a pas assez de modèles, prendre tous ceux disponibles
                top_models = list(top_models) + list(remaining_models)
        
        return top_models




#get all models accepted from the store 
class FashionModelListView(generics.ListAPIView):
    serializer_class = FashionModelSerializer2
    queryset = FashionModel.objects.all()
    
    def get_queryset(self):
        return FashionModel.objects.filter(state='accepted')
    
    
#get all women models accepted from the store 
class FashionModelFemmeListView(generics.ListAPIView):
    serializer_class = FashionModelSerializer2
    
    def get_queryset(self):
        # Filtrer seulement les modèles de type "femme" avec état "accepted"
        return FashionModel.objects.filter(type='femme', state='accepted')


#get all homme models accepted from the store 
class FashionModelHommeListView(generics.ListAPIView):
    serializer_class = FashionModelSerializer2
    
    def get_queryset(self):
        # Filtrer seulement les modèles de type "homme" avec état "accepted"
        return FashionModel.objects.filter(type='homme', state='accepted')
    

#get all enfant models accepted from the store 
class FashionModelEnfantListView(generics.ListAPIView):
    serializer_class = FashionModelSerializer2
    
    def get_queryset(self):
        # Filtrer seulement les modèles de type "enfant" avec état "accepted"
        return FashionModel.objects.filter(type='enfant', state='accepted')
    
    





# Dans views.py
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_orders(request):
    # Vérifier le rôle de l'utilisateur
    if request.user.role not in ['client']:
        return Response({"error": "Cette fonctionnalité est réservée aux clients"}, status=403)
    
    # Récupérer les commandes avec les relations nécessaires
    custom_orders = CustomOrder.objects.filter(user=request.user).prefetch_related(
        'custom_images', 'command_details'
    ).order_by('-created_at')
    
    standard_orders = Order.objects.filter(user=request.user).prefetch_related(
        'standard_command_details'
    ).select_related('fashion_model').order_by('-created_at')
    
    # Sérialiser les données
    custom_orders_data = CustomOrderSerializer(custom_orders, many=True).data
    standard_orders_data = OrderSerializer(standard_orders, many=True).data
    
    return Response({
        'custom_orders': custom_orders_data,
        'standard_orders': standard_orders_data
    })



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