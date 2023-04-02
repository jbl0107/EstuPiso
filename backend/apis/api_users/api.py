from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status


from apis.models import User
from .serializers import UserSerializer


@api_view(['GET', 'POST'])
def user_api_view(request):

    if request.method == 'GET':

        #queryset
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    #create
    elif request.method == 'POST':
        data = request.data
        serializer = UserSerializer(data = data) #many false es para indicar que realizamos un post a la vez
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET', 'PUT', 'DELETE'])
def user_detail_api_view(request, id):
        
    # queryset
    user = User.objects.filter(id=id).first()

    # validacion
    if user:
        
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        elif request.method == 'PUT':
            data = request.data
            serializer = UserSerializer(user, data = data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        elif request.method == 'DELETE':
            user.delete()
            return Response({'message':"Usuario eliminado correctamente!"}, status=status.HTTP_200_OK)
        
    return Response({'message':"No se ha encontrado un usuario con estos datos"}, status=status.HTTP_400_BAD_REQUEST)
