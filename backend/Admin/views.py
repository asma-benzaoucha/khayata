
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from Backendkadi.models.socialAccountsLinkgroups import SocialAccountsLinkGroup
from Client.serializers import SocialAccountsLinkGroupSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

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