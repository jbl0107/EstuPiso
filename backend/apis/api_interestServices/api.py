from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from apis.models import InterestService
from .serializers import InterestServiceSerializer


@api_view(['GET'])
def interestService_api_view(request):

    if request.method == 'GET':

        #queryset
        interestServices = InterestService.objects.all()
        serializer = InterestServiceSerializer(interestServices, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)

    


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def interestService_post_api_view(request):

    if request.method == 'POST':
        if request.user.isAdministrator:
            data = request.data
            serializer = InterestServiceSerializer(data = data) 
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status = status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({"message":"Debe ser administrador para crear un servicio de interés"}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def interestService_get_detail_api_view(request, id):

    interestService = InterestService.objects.filter(id=id).first()

    if interestService:

        if request.method == 'GET':
                serializer = InterestServiceSerializer(interestService)
                return Response(serializer.data, status=status.HTTP_200_OK)
        
    return Response({'message':"No se ha encontrado un servicio de interés con estos datos"}, status=status.HTTP_400_BAD_REQUEST)




@api_view(['PUT', 'DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def interestService_detail_api_view(request, id):
        
    # queryset
    interestService = InterestService.objects.filter(id=id).first()

    # validacion
    if interestService:

        if request.user.isAdministrator:
            
            if request.method == 'PUT':
                data = request.data
                serializer = InterestServiceSerializer(interestService, data = data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            elif request.method == 'DELETE':
                interestService.delete()
                return Response({'message':"Servicio de interés eliminado correctamente!"}, status=status.HTTP_200_OK)
            
        return Response({"message":"Debe ser administrador para realizar esta operación"}, status=status.HTTP_400_BAD_REQUEST)
        
    return Response({'message':"No se ha encontrado un servicio de interés con estos datos"}, status=status.HTTP_400_BAD_REQUEST)
