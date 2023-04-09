from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from apis.permissions_decorators import IsOwnerOrAdmin, IsOwner

from apis.models import Photo
from .serializers import PhotoSerializer


@api_view(['GET'])
def photo_api_view(request):

    if request.method == 'GET':

        #queryset
        photos = Photo.objects.all()
        serializer = PhotoSerializer(photos, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsOwner])
def photo_post_api_view(request):

    if request.method == 'POST': 
        data = request.data
        data['owner'] = request.user.id
        serializer = PhotoSerializer(data = data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET'])
def photo_detail_api_view(request, id):
        
    # queryset
    photo = Photo.objects.filter(id=id).first()

    # validacion
    if photo and request.method == 'GET':
        
        serializer = PhotoSerializer(photo)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
        

        
    return Response({'message':"No se ha encontrado una foto con estos datos"}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsOwnerOrAdmin])
def photo_delete_detail_api_view(request, id):

    photo = Photo.objects.filter(id=id).first()
    
    if photo and request.method == 'DELETE':
 
        if photo.owner.id == request.user.id or request.user.isAdministrator:
        
            photo.delete()
            return Response({'message':"Foto eliminada correctamente!"}, status=status.HTTP_200_OK)
            
        else:
            return Response({'message':"No puede borrar una foto de otro propietario"}, status=status.HTTP_403_FORBIDDEN)
            
        
        
    return Response({'message':"No se ha encontrado una foto con estos datos"}, status=status.HTTP_400_BAD_REQUEST)