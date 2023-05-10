from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework import status

from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from apis.permissions_decorators import IsAdmin
from rest_framework.exceptions import PermissionDenied

from apis.models import User, UserValoration, Student, Owner
from .serializers import UserSerializer
from apis.api_valoration.serializers import UserValorationSerializer


@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
def user_api_view(request):

    def check_permissions(request):

        if request.method == 'GET':
            for permission_class in [IsAuthenticated, IsAdmin]:
                permission = permission_class()
                if not permission.has_permission(request, None):
                    raise PermissionDenied(getattr(permission, 'message', None))
                
    
    check_permissions(request)


    if request.method == 'GET':

        #queryset
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    #create
    elif request.method == 'POST':
        
        data = request.data
        if data.get('isAdministrator'):
            return Response({'message':'No puede crear un administrador. Contacte con alguno para que este le de permisos de administrador'}, status=status.HTTP_403_FORBIDDEN)


        serializer = UserSerializer(data = data) #many false es para indicar que realizamos un post a la vez
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([JWTAuthentication])
def user_detail_api_view(request, id):


    def check_permissions(request):

        if request.method == 'GET':
            for permission_class in [IsAuthenticated]:
                permission = permission_class()
                if not permission.has_permission(request, None):
                    raise PermissionDenied(getattr(permission, 'message', None))

        if request.method == 'PUT':
            for permission_class in [IsAuthenticated]:
                permission = permission_class()
                if not permission.has_permission(request, None):
                    raise PermissionDenied(getattr(permission, 'message', None))
                
        elif request.method == 'DELETE':
            for permission_class in [IsAuthenticated]:
                permission = permission_class()
                if not permission.has_permission(request, None):
                    raise PermissionDenied(getattr(permission, 'message', None))

    check_permissions(request)
        
    # queryset
    user = User.objects.filter(id=id).first()

    # validacion
    if user:
        
        if request.method == 'GET':
            if not (request.user.id == id or request.user.isAdministrator):
                return Response({'message':'Solo puede ver sus datos, no puede ver información ajena'}, status=status.HTTP_403_FORBIDDEN)


            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        elif request.method == 'PUT':

            if not (request.user.id == id or request.user.isAdministrator):
                return Response({'message':'Solo puede actualizar sus datos, no puede actualizar información ajena'}, status=status.HTTP_403_FORBIDDEN)
            
            aux1 = user.isActive
            aux2 = user.isAdministrator

            if not aux1 and not aux2:
                return Response({'message':'No puede actualizar su información, su cuenta ha sido desactivada'}, status=status.HTTP_403_FORBIDDEN)

            

            data = request.data
            
            if data.get('isAdministrator') and aux2 == False and not request.user.isAdministrator:
                return Response({'message':'No puede hacerse administrador a si mismo'}, status=status.HTTP_403_FORBIDDEN)

            if data.get('isActive') == False and not request.user.isAdministrator:
                return Response({'message':'No puede desactivar su cuenta sin ser administrador'}, status=status.HTTP_403_FORBIDDEN)


            serializer = UserSerializer(user, data = data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

        elif request.method == 'DELETE':

            if not (request.user.id == id or request.user.isAdministrator):
                return Response({'message':'Solo puede borrar sus datos, no puede borrar información ajena'}, status=status.HTTP_403_FORBIDDEN)
            
            user.delete()
            return Response({'message':"Usuario eliminado correctamente!"}, status=status.HTTP_200_OK)
        
    return Response({'message':"No se ha encontrado un usuario con estos datos"}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def user_valoration_received_api_view(request, id):

    user = User.objects.filter(id=id).first()

    if user:

        if request.method == 'GET':

            #queryset
            valorations = UserValoration.objects.all()
            res = []
            
            for v in valorations:
                if v.valued == user:
                    res.append(v)

            serializer = UserValorationSerializer(res, many=True)
            return Response(serializer.data, status = status.HTTP_200_OK)
    

    return Response({'message': "No se ha encontrado un usuario con estos datos"}, status=status.HTTP_400_BAD_REQUEST) 



@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def user_valoration_done_to_users_api_view(request, id):

    user = User.objects.filter(id=id).first()

    if user:

        if request.method == 'GET':

            if not (request.user.id == id or request.user.isAdministrator):
                return Response({'message':'Solo puede obtener un listado de todas sus valoraciones, no de otros usuarios'}, status=status.HTTP_403_FORBIDDEN)

            #queryset
            res = UserValoration.objects.filter(valuer=user)
            serializer = UserValorationSerializer(res, many=True)
            return Response(serializer.data, status = status.HTTP_200_OK)
    

    return Response({'message': "No se ha encontrado un usuario con estos datos"}, status=status.HTTP_400_BAD_REQUEST) 



@api_view(['GET'])
def get_user_type(request, id):

    if Student.objects.filter(id=id).exists():
        user_type = 'student'
    
    elif Owner.objects.filter(id=id).exists():
        user_type = 'owner'
    
    else:
        user_type = None
    
    return Response({'userType': user_type}, status=status.HTTP_200_OK)