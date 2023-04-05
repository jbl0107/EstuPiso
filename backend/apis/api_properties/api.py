from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status


from apis.models import Property, PropertyValoration
from .serializers import PropertySerializer
from apis.api_rules.serializers import RuleSerializer
from apis.api_photos.serializers import PhotoSerializer
from apis.api_services.serializers import ServiceSerializer
from apis.api_valoration.serializers import PropertyValorationSerializer


@api_view(['GET', 'POST'])
def property_api_view(request):

    if request.method == 'GET':

        #queryset
        properties = Property.objects.all()
        serializer = PropertySerializer(properties, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    #create
    elif request.method == 'POST':
        data = request.data
        serializer = PropertySerializer(data = data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET', 'PUT', 'DELETE'])
def property_detail_api_view(request, id):
        
    # queryset
    property = Property.objects.filter(id=id).first()

    # validacion
    if property:
        
        if request.method == 'GET':
            serializer = PropertySerializer(property)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        elif request.method == 'PUT':
            data = request.data
            serializer = PropertySerializer(property, data = data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        elif request.method == 'DELETE':
            property.delete()
            return Response({'message':"Inmueble eliminado correctamente!"}, status=status.HTTP_200_OK)
        
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