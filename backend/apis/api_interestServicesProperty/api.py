from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status

from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from apis.models import InterestServiceProperty, Property
from .serializers import InterestServicePropertySerializer


@api_view(['GET'])
def interestServiceProperty_api_view(request):

    if request.method == 'GET':

        interestServicesProperty = InterestServiceProperty.objects.all()
        serializer = InterestServicePropertySerializer(interestServicesProperty, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    




@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def interestServiceProperty_post_api_view(request):

    if request.method == 'POST':

        if not request.user.isAdministrator:
            return Response({"message":"Debe ser administrador para crear un servicio de interés de un inmueble"}, status=status.HTTP_400_BAD_REQUEST)
        
        data = request.data
        serializer = InterestServicePropertySerializer(data = data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['GET'])
def interestServiceProperty_get_detail_api_view(request, id):
 
    interestServiceProperty = InterestServiceProperty.objects.filter(id=id).first()

    if interestServiceProperty:
        
        if request.method == 'GET':
            serializer = InterestServicePropertySerializer(interestServiceProperty)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
    return Response({'message':"No se ha encontrado un servicio de interés de una propiedad con estos datos"}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['PUT', 'DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def interestServiceProperty_detail_api_view(request, id):
        
    # queryset
    interestServiceProperty = InterestServiceProperty.objects.filter(id=id).first()

    # validacion
    if interestServiceProperty:
        
        if not request.user.isAdministrator:
            return Response({"message":"Debe ser administrador para poder realizar esta operación"}, status=status.HTTP_400_BAD_REQUEST)
        
        
        if request.method == 'PUT':
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
            all_interestServicesProperty = InterestServiceProperty.objects.all()
            res=[]

            for isp in all_interestServicesProperty:
                if isp.property == property:
                    res.append(isp)

            serializer = InterestServicePropertySerializer(res, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
    return Response({'message':"No se ha encontrado una propiedad con estos datos"}, status=status.HTTP_400_BAD_REQUEST)
