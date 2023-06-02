from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from apis.permissions_decorators import IsOwnerOrAdmin, IsOwner
from rest_framework.exceptions import PermissionDenied


from apis.models import Photo, Owner
from .serializers import PhotoSerializer


@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
def photo_api_view(request):

    def check_permissions(request):

        if request.method == 'POST':
            for permission_class in [IsAuthenticated, IsOwner]:
                permission = permission_class()
                if not permission.has_permission(request, None):
                    raise PermissionDenied(getattr(permission, 'message', None))
                
    
    check_permissions(request)

    if request.method == 'GET':

        #queryset
        photos = Photo.objects.all()
        serializer = PhotoSerializer(photos, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    

    if request.method == 'POST': 
        data = request.data
        data['owner'] = request.user.id
        serializer = PhotoSerializer(data = data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    



@api_view(['GET', 'DELETE'])
@authentication_classes([JWTAuthentication])
def photo_detail_api_view(request, id):

    def check_permissions(request):
        
        if request.method == 'DELETE':
            for permission_class in [IsAuthenticated, IsOwnerOrAdmin]:
                permission = permission_class()
                if not permission.has_permission(request, None):
                    raise PermissionDenied(getattr(permission, 'message', None))
                
    
    check_permissions(request)
        
    # queryset
    photo = Photo.objects.filter(id=id).first()

    # validacion
    if photo:

        if request.method == 'GET':
            serializer = PhotoSerializer(photo)
            return Response(serializer.data, status=status.HTTP_200_OK)
        

        elif request.method == 'DELETE':

            if photo.owner.id == request.user.id or request.user.isAdministrator:
        
                photo.delete()
                return Response({'message':"Foto eliminada correctamente!"}, status=status.HTTP_200_OK)
            
            else:
                return Response({'message':"No puede borrar una foto de otro propietario"}, status=status.HTTP_403_FORBIDDEN)
        

        
    return Response({'message':"No se ha encontrado una foto con estos datos"}, status=status.HTTP_404_NOT_FOUND)



@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsOwnerOrAdmin])
def photo_owner_detail_api_view(request, id):

    owner = Owner.objects.filter(id=id)
    print(owner)
    if owner:
         
         if request.method == 'GET':
            if not (request.user.id == id or request.user.isAdministrator):
                return Response({'message':"No puede ver todas las fotos de inmuebles de otro propietario"}, status=status.HTTP_403_FORBIDDEN)
            
            photos = Photo.objects.filter(owner__in=owner)
            serializer = PhotoSerializer(photos, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
         
    return Response({'message':"No se ha encontrado un propietario con estos datos"}, status=status.HTTP_404_NOT_FOUND)


