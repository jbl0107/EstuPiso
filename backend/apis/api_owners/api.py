from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from apis.permissions_decorators import IsOwnerOrAdmin

from apis.models import Owner, Property
from .serializers import OwnerSerializer
from apis.api_properties.serializers import PropertySerializer


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def owner_api_view(request):

    if request.method == 'GET':

        if request.user.isAdministrator:
        #queryset
            owners = Owner.objects.all()
            serializer = OwnerSerializer(owners, many=True)
            return Response(serializer.data, status = status.HTTP_200_OK)
        
        else:
            return Response({'message':"Usted no es administrador"}, status=status.HTTP_403_FORBIDDEN)
  



@api_view(['POST'])
def owner_post_api_view(request):

    if request.method == 'POST':
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
                serializer = OwnerSerializer(owner, data = data)
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
        

    return Response({'message':"No se ha encontrado un propietario con estos datos"}, status=status.HTTP_400_BAD_REQUEST)



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
        
    return Response({'message': 'No se ha encontrado un propietario con estos datos'}, status=status.HTTP_400_BAD_REQUEST)

