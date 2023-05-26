from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from apis.permissions_decorators import IsOwnerOrAdmin, IsOwner

from rest_framework.exceptions import PermissionDenied

from apis.models import Property, PropertyValoration, PropertyType
from .serializers import PropertySerializer
from apis.api_rules.serializers import RuleSerializer
from apis.api_photos.serializers import PhotoSerializer
from apis.api_services.serializers import ServiceSerializer
from apis.api_valoration.serializers import PropertyValorationSerializer


@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
def property_api_view(request):

    def check_permissions(request):
        if request.method == 'POST':
            for permission_class in [IsAuthenticated, IsOwner]:
                permission = permission_class()
                if not permission.has_permission(request, None):
                    raise PermissionDenied(getattr(permission, 'message', None))
                
    
    check_permissions(request)

    if request.method == 'GET':

        properties = Property.objects.all()
        serializer = PropertySerializer(properties, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    #create
    elif request.method == 'POST':
        data = request.data
        data = request.POST.copy()
        data['owner'] = request.user.id
        serializer = PropertySerializer(data = data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    





@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([JWTAuthentication])
def property_detail_api_view(request, id):

    def check_permissions(request):
        if request.method == 'PUT':
            for permission_class in [IsAuthenticated, IsOwner]:
                permission = permission_class()
                if not permission.has_permission(request, None):
                    raise PermissionDenied(getattr(permission, 'message', None))
                
        elif request.method == 'DELETE':
            for permission_class in [IsAuthenticated, IsOwnerOrAdmin]:
                permission = permission_class()
                if not permission.has_permission(request, None):
                    raise PermissionDenied(getattr(permission, 'message', None))

    check_permissions(request)

        
    # queryset
    property = Property.objects.filter(id=id).first()

    # validacion
    if property:

        aux = request.user.id == property.owner.id

        if request.method == 'GET':

            serializer = PropertySerializer(property)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        
        elif request.method == 'PUT':

            if not aux:
                return Response({"message":"No puede actualizar los datos de un inmueble de otro propietario"}, status=status.HTTP_403_FORBIDDEN)
           
            data = request.data
            data['owner'] = request.user.id
            serializer = PropertySerializer(property, data = data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
        elif request.method == 'DELETE':
            if aux or request.user.isAdministrator:
                property.delete()
                return Response({'message':"Inmueble eliminado correctamente!"}, status=status.HTTP_200_OK)
            
            else:
                return Response({"message":"No puede borrar un inmueble de otro propietario"}, status=status.HTTP_403_FORBIDDEN)
             
        
    return Response({'message':"No se ha encontrado un inmueble con estos datos"}, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET'])
def property_rules_api_view(request, id):

    property = Property.objects.filter(id=id).first()

    if property:

        if request.method == 'GET':
            rules = property.rules
            serializer = RuleSerializer(rules, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        
    return Response({'message': "No se ha encontrado un inmueble con estos datos"}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def property_photos_api_view(request, id):

    property = Property.objects.filter(id=id).first()

    if property:

        if request.method == 'GET':
            photos = property.photos
            serializer = PhotoSerializer(photos, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        
    return Response({'message': "No se ha encontrado un inmueble con estos datos"}, status=status.HTTP_400_BAD_REQUEST) 


@api_view(['GET'])
def property_services_api_view(request, id):

    property = Property.objects.filter(id=id).first()

    if property:

        if request.method == 'GET':
            services = property.services
            serializer = ServiceSerializer(services, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        
    return Response({'message': "No se ha encontrado un inmueble con estos datos"}, status=status.HTTP_400_BAD_REQUEST) 



@api_view(['GET'])
def property_valorations_api_view(request, id):

    property = Property.objects.filter(id=id).first()

    if property:

        if request.method == 'GET':

            #queryset
            valorations = PropertyValoration.objects.all()
            res = []
            
            for v in valorations:
                if v.property == property:
                    res.append(v)

            serializer = PropertyValorationSerializer(res, many=True)
            return Response(serializer.data, status = status.HTTP_200_OK)
    

    return Response({'message': "No se ha encontrado un inmueble con estos datos"}, status=status.HTTP_400_BAD_REQUEST) 



@api_view(["GET"])
def property_types(request):
    property_types = [choice.value for choice in PropertyType]
    return Response(property_types)