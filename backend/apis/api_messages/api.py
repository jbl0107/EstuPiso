from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


from apis.models import Message, User
from .serializers import MessageSerializer


@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def message_api_view(request):

    if request.method == 'GET':
        
        if not request.user.isAdministrator:
            return Response({'message': 'No puede obtener los mensajes del resto de usuarios registrados'}, status=status.HTTP_400_BAD_REQUEST) 

        #queryset
        messages = Message.objects.all()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    #create
    elif request.method == 'POST':

        data = request.data
        if request.user.id == int(data.get('userSender')) or request.user.isAdministrator:

            serializer = MessageSerializer(data = data) 
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status = status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            return Response({'message': 'No puede enviar un mensaje en nombre de otro usuario'}, status=status.HTTP_400_BAD_REQUEST)





@api_view(['GET', 'DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def message_detail_api_view(request, id):
        
    # queryset
    message = Message.objects.filter(id=id).first()

    # validacion
    if message:
        

        if request.method == 'GET':
            if (request.user.id == message.userSender.id or request.user.id == message.userRecipient.id) or request.user.isAdministrator:
                serializer = MessageSerializer(message)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'message':"No puede obtener mensajes en los que no esté involucrado"}, status=status.HTTP_400_BAD_REQUEST)
    
        
        elif request.method == 'DELETE':
            if request.user.id == message.userSender.id or request.user.isAdministrator:
            
                message.delete()
                return Response({'message':"Mensaje eliminado correctamente!"}, status=status.HTTP_200_OK)

            else:
                return Response({'message':"No puede borrar un mensaje que no haya enviado"}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({'message':"No se ha encontrado un mensaje con estos datos"}, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def message_user_api_view(request, id_user):
        
    # queryset
    user = User.objects.filter(id=id_user).first()


    # validacion
    if user:
        
        if request.method == 'GET':

            if request.user.id == id_user or request.user.isAdministrator:

                messages = Message.objects.all()
                res = []

                for m in messages:
                    if m.userSender == user or m.userRecipient == user:
                        res.append(m)


                serializer = MessageSerializer(res, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            else:
                return Response({'message':"No puede ver los mensajes de otros usuarios"}, status=status.HTTP_400_BAD_REQUEST)

        
    return Response({'message':"El usuario no existe"}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def message_user_conversation_api_view(request, id_user1, id_user2):
        
    # queryset
    user1 = User.objects.filter(id=id_user1).first()
    user2 = User.objects.filter(id=id_user2).first()


    # validacion
    if user1 and user2:
        
        if request.method == 'GET':

            if (request.user.id == id_user1 or request.user.id == id_user2) or request.user.isAdministrator:
                messages = Message.objects.all()
                res = []

                for m in messages:
                    if (m.userSender == user1 and m.userRecipient == user2) or (m.userSender == user2 and m.userRecipient == user1):
                        res.append(m)
                
                serializer = MessageSerializer(res, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            return Response({'message':"No puede obtener una conversación en la que no es participe"}, status=status.HTTP_400_BAD_REQUEST)

        
    return Response({'message':"Alguno de los usuarios no existe"}, status=status.HTTP_400_BAD_REQUEST)