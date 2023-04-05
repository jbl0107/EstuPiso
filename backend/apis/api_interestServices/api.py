from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status


from apis.models import InterestService
from .serializers import InterestServiceSerializer


@api_view(['GET', 'POST'])
def interestService_api_view(request):

    if request.method == 'GET':

        #queryset
        interestServices = InterestService.objects.all()
        serializer = InterestServiceSerializer(interestServices, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    #create
    elif request.method == 'POST':
        data = request.data
        serializer = InterestServiceSerializer(data = data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET', 'PUT', 'DELETE'])
def interestService_detail_api_view(request, id):
        
    # queryset
    interestService = InterestService.objects.filter(id=id).first()

    # validacion
    if interestService:
        
        if request.method == 'GET':
            serializer = InterestServiceSerializer(interestService)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        elif request.method == 'PUT':
            data = request.data
            serializer = InterestServiceSerializer(interestService, data = data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        elif request.method == 'DELETE':
            interestService.delete()
            return Response({'message':"Servicio de interés eliminado correctamente!"}, status=status.HTTP_200_OK)
        
    return Response({'message':"No se ha encontrado un servicio de interés con estos datos"}, status=status.HTTP_400_BAD_REQUEST)
