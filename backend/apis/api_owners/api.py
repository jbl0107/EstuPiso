from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from apis.permissions_decorators import IsOwnerOrAdmin, IsAdmin, IsStudentOrAdmin, IsOwner
from rest_framework.exceptions import PermissionDenied


from apis.models import Owner, Property
from .serializers import OwnerSerializer, OwnerPublicSerializer, OwnerStudentSerializer, OwnerUpdateSerializer
from apis.api_properties.serializers import PropertySerializer

from django.contrib.auth.hashers import check_password
from rest_framework.exceptions import NotAuthenticated




@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
def owner_api_view(request):

    def check_permissions(request):

        if request.method == 'GET':
            if 'HTTP_AUTHORIZATION' not in request.META:
                raise NotAuthenticated()
            for permission_class in [IsAuthenticated, IsAdmin]:
                permission = permission_class()
                if not permission.has_permission(request, None):
                    raise PermissionDenied(getattr(permission, 'message', None))
                
    
    check_permissions(request)

    if request.method == 'GET':

        #queryset
        owners = Owner.objects.all()
        serializer = OwnerSerializer(owners, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
  

    elif request.method == 'POST':
        data = request.data
        serializer = OwnerSerializer(data = data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsOwnerOrAdmin])
def owner_detail_api_view(request, id):
        
    # queryset
    owner = Owner.objects.filter(id=id).first()

    # validacion
    if owner:

        aux = request.user.id == owner.id or request.user.isAdministrator

        if request.method == 'GET':
            if aux:
                serializer = OwnerSerializer(owner)
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            else:
                return Response({'message':"No puede obtener los datos de otro propietario que no sea usted mismo"}, status=status.HTTP_403_FORBIDDEN)
        
        elif request.method == 'PUT':
            if aux:
                data = request.data
                serializer = OwnerUpdateSerializer(owner, data = data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            else:
                return Response({'message':"No puede cambiar los datos de otro propietario que no sea usted mismo"}, status=status.HTTP_403_FORBIDDEN)
        
        elif request.method == 'DELETE':

            if aux:
                owner.delete()
                return Response({'message':"Propietario eliminado correctamente!"}, status=status.HTTP_200_OK)
        
            else:
                return Response({'message':"No puede borrar a otro propietario que no sea usted mismo"}, status=status.HTTP_403_FORBIDDEN)
        

    return Response({'message':"No se ha encontrado un propietario con estos datos"}, status=status.HTTP_404_NOT_FOUND)



@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsOwnerOrAdmin])
def owner_properties_api_view(request, id):

    owner = Owner.objects.filter(id=id).first()

    if owner:
        
        if request.method == 'GET':

            if request.user.id == owner.id or request.user.isAdministrator:
      
                res = Property.objects.filter(owner=owner)
                serializer = PropertySerializer(res, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            else:
                return Response({'message':"Solo puede obtener todas sus propiedades"}, status=status.HTTP_403_FORBIDDEN)
        
    return Response({'message': 'No se ha encontrado un propietario con estos datos'}, status=status.HTTP_404_NOT_FOUND)




@api_view(['GET'])
def owner_public_detail_api_view(request, id):
        
    # queryset
    owner = Owner.objects.filter(id=id).first()

    # validacion
    if owner:

        if request.method == 'GET':
            serializer = OwnerPublicSerializer(owner)
            return Response(serializer.data, status=status.HTTP_200_OK)
            

    return Response({'message':"No se ha encontrado un propietario con estos datos"}, status=status.HTTP_404_NOT_FOUND)



@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsStudentOrAdmin])
def owner_student_detail_api_view(request, id):
        
    # queryset
    owner = Owner.objects.filter(id=id).first()

    # validacion
    if owner:

        if request.method == 'GET':
            serializer = OwnerStudentSerializer(owner)
            return Response(serializer.data, status=status.HTTP_200_OK)
            

    return Response({'message':"No se ha encontrado un propietario con estos datos"}, status=status.HTTP_404_NOT_FOUND)



@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsOwner])
def owner_verify_password(request):
    # Obtener la contraseña introducida por el usuario desde la solicitud
    entered_password = request.data.get('password')
    
    # Obtener el usuario y la contraseña encriptada almacenada en la base de datos
    user = Owner.objects.get(username=request.user.username)
    stored_password = user.password
    
    # Verificar si las contraseñas coinciden
    if check_password(entered_password, stored_password):
        
        # Las contraseñas coinciden
        return Response({'password_correct': True})
    else:
        return Response({'password_correct': False})
    


@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsOwner])
def owner_profile_change_password(request):

    new_password = request.data.get('new_password')

    if len(new_password) < 8:
        return Response({'message': 'La contraseña debe tener al menos 8 caracteres'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = Owner.objects.get(username=request.user.username)
        user.set_password(new_password)
        user.save()
        return Response({'message': 'Contraseña actualizada correctamente'}, status=status.HTTP_200_OK)
    except Owner.DoesNotExist:
        return Response({'message': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)



@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsOwnerOrAdmin])
def owner_photo_update(request, id):
    owner = Owner.objects.filter(id=id).first()
    if owner:
        aux = request.user.id == owner.id
        if not (aux or request.user.isAdministrator):
            return Response({'message':"No puede actualizar la foto de otro propietario!"}, status=status.HTTP_403_FORBIDDEN)
        data = request.data
        serializer = OwnerUpdateSerializer(owner, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({'message':"No se ha encontrado un propietario con estos datos"}, status=status.HTTP_404_NOT_FOUND)