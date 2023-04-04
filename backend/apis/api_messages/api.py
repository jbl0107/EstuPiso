from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status


from apis.models import Message, User
from .serializers import MessageSerializer


@api_view(['GET', 'POST'])
def message_api_view(request):

    if request.method == 'GET':

        #queryset
        messages = Message.objects.all()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    #create
    elif request.method == 'POST':
        data = request.data
        serializer = MessageSerializer(data = data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET', 'DELETE'])
def message_detail_api_view(request, id):
        
    # queryset
    message = Message.objects.filter(id=id).first()

    # validacion
    if message:
        
        if request.method == 'GET':
            serializer = MessageSerializer(message)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        
        elif request.method == 'DELETE':
            message.delete()
            return Response({'message':"Mensaje eliminado correctamente!"}, status=status.HTTP_200_OK)
        
    return Response({'message':"No se ha encontrado un mensaje con estos datos"}, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET'])
def message_user_api_view(request, id_user):
        
    # queryset
    user = User.objects.filter(id=id_user).first()


    # validacion
    if user:
        
        if request.method == 'GET':
            messages = Message.objects.all()
            res = []

            for m in messages:
                if m.userSender == user or m.userRecipient == user:
                    res.append(m)

            serializer = MessageSerializer(res, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        
    return Response({'message':"El usuario no existe"}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def message_user_conversation_api_view(request, id_user1, id_user2):
        
    # queryset
    user1 = User.objects.filter(id=id_user1).first()
    user2 = User.objects.filter(id=id_user2).first()


    # validacion
    if user1 and user2:
        
        if request.method == 'GET':
            messages = Message.objects.all()
            res = []

            for m in messages:
                if (m.userSender == user1 and m.userRecipient == user2) or (m.userSender == user2 and m.userRecipient == user1):
                    res.append(m)
            
            serializer = MessageSerializer(res, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        
    return Response({'message':"Alguno/s de los usuarios no existen"}, status=status.HTTP_400_BAD_REQUEST)