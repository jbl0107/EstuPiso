from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status


from apis.models import Owner, Property
from .serializers import OwnerSerializer
from apis.api_properties.serializers import PropertySerializer


@api_view(['GET', 'POST'])
def owner_api_view(request):

    if request.method == 'GET':

        #queryset
        owners = Owner.objects.all()
        serializer = OwnerSerializer(owners, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    #create
    elif request.method == 'POST':
        data = request.data
        serializer = OwnerSerializer(data = data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET', 'PUT', 'DELETE'])
def owner_detail_api_view(request, id):
        
    # queryset
    owner = Owner.objects.filter(id=id).first()

    # validacion
    if owner:
        
        if request.method == 'GET':
            serializer = OwnerSerializer(owner)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        elif request.method == 'PUT':
            data = request.data
            serializer = OwnerSerializer(owner, data = data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        elif request.method == 'DELETE':
            owner.delete()
            return Response({'message':"Propietario eliminado correctamente!"}, status=status.HTTP_200_OK)
        
    return Response({'message':"No se ha encontrado un propietario con estos datos"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def owner_properties_api_view(request, id):

    owner = Owner.objects.filter(id=id).first()

    if owner:
        
        if request.method == 'GET':
            all_properties = Property.objects.all()
            res = []

            for p in all_properties:
                if p.owner == owner:
                    res.append(p)
            
            serializer = PropertySerializer(res, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
    return Response({'message': 'No se ha encontrado un propietario con estos datos'}, status=status.HTTP_400_BAD_REQUEST)

