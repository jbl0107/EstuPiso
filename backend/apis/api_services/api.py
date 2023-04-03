from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status


from apis.models import Service
from .serializers import ServiceSerializer


@api_view(['GET', 'POST'])
def service_api_view(request):

    if request.method == 'GET':

        #queryset
        services = Service.objects.all()
        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    #create
    elif request.method == 'POST':
        data = request.data
        serializer = ServiceSerializer(data = data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET', 'PUT', 'DELETE'])
def service_detail_api_view(request, id):
        
    # queryset
    service = Service.objects.filter(id=id).first()

    # validacion
    if service:
        
        if request.method == 'GET':
            serializer = ServiceSerializer(service)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        elif request.method == 'PUT':
            data = request.data
            serializer = ServiceSerializer(service, data = data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        elif request.method == 'DELETE':
            service.delete()
            return Response({'message':"Servicio eliminado correctamente!"}, status=status.HTTP_200_OK)
        
    return Response({'message':"No se ha encontrado un servicio con estos datos"}, status=status.HTTP_400_BAD_REQUEST)
