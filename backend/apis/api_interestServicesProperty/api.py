from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status

from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from apis.models import InterestServiceProperty, Property
from .serializers import InterestServicePropertySerializer
from rest_framework.exceptions import PermissionDenied
from apis.permissions_decorators import IsOwnerOrAdmin, IsAdmin




@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
def interestServiceProperty_api_view(request):

    def check_permissions(request):
        
        if request.method == 'POST':
            for permission_class in [IsAuthenticated, IsAdmin]:
                permission = permission_class()
                if not permission.has_permission(request, None):
                    raise PermissionDenied(getattr(permission, 'message', None))
                
    
    check_permissions(request)

    if request.method == 'GET':

        interestServicesProperty = InterestServiceProperty.objects.all()
        serializer = InterestServicePropertySerializer(interestServicesProperty, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    if request.method == 'POST':

        data = request.data
        serializer = InterestServicePropertySerializer(data = data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        
       
        


# get sin restriccion
@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([JWTAuthentication])
def interestServiceProperty_detail_api_view(request, id):

    def check_permissions(request):
        
        if request.method == 'PUT':
            for permission_class in [IsAuthenticated, IsAdmin]:
                permission = permission_class()
                if not permission.has_permission(request, None):
                    raise PermissionDenied(getattr(permission, 'message', None))
                
        elif request.method == 'DELETE':
            for permission_class in [IsAuthenticated, IsAdmin]:
                permission = permission_class()
                if not permission.has_permission(request, None):
                    raise PermissionDenied(getattr(permission, 'message', None))
                
        
    check_permissions(request)

        
    # queryset
    interestServiceProperty = InterestServiceProperty.objects.filter(id=id).first()

    # validacion
    if interestServiceProperty:
        
        if request.method == 'GET':
            serializer = InterestServicePropertySerializer(interestServiceProperty)
            return Response(serializer.data, status=status.HTTP_200_OK)

        elif request.method == 'PUT':
            data = request.data
            serializer = InterestServicePropertySerializer(interestServiceProperty, data = data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        elif request.method == 'DELETE':
            interestServiceProperty.delete()
            return Response({'message':"Servicio de interés de una propiedad eliminado correctamente!"}, status=status.HTTP_200_OK)
        
    return Response({'message':"No se ha encontrado un servicio de interés de una propiedad con estos datos"}, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET'])
def interestServiceProperty_property_api_view(request, id):
        
    # queryset
    property = Property.objects.filter(id=id).first()

    # validacion
    if property:
        
        if request.method == 'GET':
            res = InterestServiceProperty.objects.filter(property=property)
            serializer = InterestServicePropertySerializer(res, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
    return Response({'message':"No se ha encontrado una propiedad con estos datos"}, status=status.HTTP_400_BAD_REQUEST)
