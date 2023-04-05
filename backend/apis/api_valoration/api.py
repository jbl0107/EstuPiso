from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status


from apis.models import UserValoration, PropertyValoration
from .serializers import UserValorationSerializer, PropertyValorationSerializer

##################################################
#Users

@api_view(['GET', 'POST'])
def valoration_user_api_view(request):

    if request.method == 'GET':

        #queryset
        valorations = UserValoration.objects.all()
        serializer = UserValorationSerializer(valorations, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    #create
    elif request.method == 'POST':
        data = request.data
        serializer = UserValorationSerializer(data = data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET', 'DELETE'])
def valoration_user_detail_api_view(request, id):
        
    # queryset
    valoration = UserValoration.objects.filter(id=id).first()

    # validacion
    if valoration:
        
        if request.method == 'GET':
            serializer = UserValorationSerializer(valoration)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        
        elif request.method == 'DELETE':
            valoration.delete()
            return Response({'message':"Valoración a usuario eliminada correctamente!"}, status=status.HTTP_200_OK)
        
    return Response({'message':"No se ha encontrado una valoración a un usuario con estos datos"}, status=status.HTTP_400_BAD_REQUEST)




#########################################
# Properties

@api_view(['GET', 'POST'])
def valoration_property_api_view(request):

    if request.method == 'GET':

        #queryset
        valorations = PropertyValoration.objects.all()
        serializer = PropertyValorationSerializer(valorations, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    #create
    elif request.method == 'POST':
        data = request.data
        serializer = PropertyValorationSerializer(data = data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET', 'DELETE'])
def valoration_property_detail_api_view(request, id):
        
    # queryset
    valoration = PropertyValoration.objects.filter(id=id).first()

    # validacion
    if valoration:
        
        if request.method == 'GET':
            serializer = PropertyValorationSerializer(valoration)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        
        elif request.method == 'DELETE':
            valoration.delete()
            return Response({'message':"Valoración a un inmueble eliminada correctamente!"}, status=status.HTTP_200_OK)
        
    return Response({'message':"No se ha encontrado una valoración a un inmueble con estos datos"}, status=status.HTTP_400_BAD_REQUEST)
