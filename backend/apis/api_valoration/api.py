from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework import status

from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from apis.models import UserValoration, PropertyValoration, Owner
from .serializers import UserValorationSerializer, PropertyValorationSerializer

##################################################
#Users

@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def valoration_user_api_view(request):

    if request.method == 'GET':

        #queryset
        valorations = UserValoration.objects.all()
        serializer = UserValorationSerializer(valorations, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    #create
    elif request.method == 'POST':
        
        data = request.data
        data['valuer'] = request.user.id

        if data['valuer'] == int(data['valued']):
            return Response({'message':'No puede valorarse a si mismo'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = UserValorationSerializer(data = data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET', 'DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def valoration_user_detail_api_view(request, id):
        
    # queryset
    valoration = UserValoration.objects.filter(id=id).first()

    # validacion
    if valoration:
        
        if request.method == 'GET':
            serializer = UserValorationSerializer(valoration)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        
        elif request.method == 'DELETE':
            if not (request.user.id == valoration.valuer.id or request.user.isAdministrator):
                return Response({"message":"No puede borrar una valoración de otro usuario registrado"}, status=status.HTTP_403_FORBIDDEN)

            valoration.delete()
            return Response({'message':"Valoración a usuario eliminada correctamente!"}, status=status.HTTP_200_OK)
        
    return Response({'message':"No se ha encontrado una valoración a un usuario con estos datos"}, status=status.HTTP_404_NOT_FOUND)




#########################################
# Properties

@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def valoration_property_api_view(request):

    if request.method == 'GET':

        #queryset
        valorations = PropertyValoration.objects.all()
        serializer = PropertyValorationSerializer(valorations, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    #create
    elif request.method == 'POST':
       
        data = request.data
        data['valuer'] = request.user.id
        
        if Owner.objects.filter(id=data['valuer']).exists():
            return Response({'message':"Un propietario no puede valorar inmuebles"}, status=status.HTTP_403_FORBIDDEN)
        
        if request.user.isAdministrator:
            return Response({'message':"Un administrador no puede valorar inmuebles"}, status=status.HTTP_403_FORBIDDEN)


        serializer = PropertyValorationSerializer(data = data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)




@api_view(['GET', 'DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def valoration_property_detail_api_view(request, id):
        
    # queryset
    valoration = PropertyValoration.objects.filter(id=id).first()

    # validacion
    if valoration:
        
        if request.method == 'GET':
            serializer = PropertyValorationSerializer(valoration)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        
        elif request.method == 'DELETE':
            if not (request.user.id == valoration.valuer.id or request.user.isAdministrator):
                return Response({"message":"No puede borrar una valoración de otro estudiante"}, status=status.HTTP_403_FORBIDDEN)

            valoration.delete()
            return Response({'message':"Valoración a un inmueble eliminada correctamente!"}, status=status.HTTP_200_OK)
        
    return Response({'message':"No se ha encontrado una valoración a un inmueble con estos datos"}, status=status.HTTP_404_NOT_FOUND)
