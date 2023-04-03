from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status


from apis.models import Photo
from .serializers import PhotoSerializer


@api_view(['GET', 'POST'])
def photo_api_view(request):

    if request.method == 'GET':

        #queryset
        photos = Photo.objects.all()
        serializer = PhotoSerializer(photos, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    #create
    elif request.method == 'POST':
        data = request.data
        serializer = PhotoSerializer(data = data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET', 'PUT', 'DELETE'])
def photo_detail_api_view(request, id):
        
    # queryset
    photo = Photo.objects.filter(id=id).first()

    # validacion
    if photo:
        
        if request.method == 'GET':
            serializer = PhotoSerializer(photo)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        elif request.method == 'PUT':
            data = request.data
            serializer = PhotoSerializer(photo, data = data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        elif request.method == 'DELETE':
            photo.delete()
            return Response({'message':"Foto eliminada correctamente!"}, status=status.HTTP_200_OK)
        
    return Response({'message':"No se ha encontrado una foto con estos datos"}, status=status.HTTP_400_BAD_REQUEST)
