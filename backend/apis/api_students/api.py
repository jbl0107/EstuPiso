from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework import status

from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from apis.permissions_decorators import IsStudentOrAdmin, IsAdmin, IsStudent
from rest_framework.exceptions import PermissionDenied

from apis.models import Student, PropertyValoration
from .serializers import StudentSerializer, StudentUpdateSerializer
from apis.api_valoration.serializers import PropertyValorationSerializer

from django.contrib.auth.hashers import check_password




@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
def student_api_view(request):


    def check_permissions(request):

        if request.method == 'GET':
            for permission_class in [IsAuthenticated, IsAdmin]:
                permission = permission_class()
                if not permission.has_permission(request, None):
                    raise PermissionDenied(getattr(permission, 'message', None))
                
    
    check_permissions(request)

    if request.method == 'GET':

        #queryset
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    #create
    elif request.method == 'POST':
        data = request.data
        serializer = StudentSerializer(data = data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsStudentOrAdmin])
def student_detail_api_view(request, id):
        
    # queryset
    student = Student.objects.filter(id=id).first()

    # validacion
    if student:

        aux = request.user.id == student.id

        if request.method == 'GET':

            if not (aux or request.user.isAdministrator):
                return Response({'message':"No puede acceder a los datos de otro estudiante!"}, status=status.HTTP_403_FORBIDDEN)
            
            serializer = StudentSerializer(student)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        elif request.method == 'PUT':
            if not (aux or request.user.isAdministrator):
                return Response({'message':"No puede actualizar los datos de otro estudiante!"}, status=status.HTTP_403_FORBIDDEN)
            
            data = request.data
            serializer = StudentUpdateSerializer(student, data = data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

        elif request.method == 'DELETE':
            if not (aux or request.user.isAdministrator):
                return Response({'message':"No puede elminiar a otro estudiante!"}, status=status.HTTP_403_FORBIDDEN)
            
            student.delete()
            return Response({'message':"Estudiante eliminado correctamente!"}, status=status.HTTP_200_OK)
        
    return Response({'message':"No se ha encontrado un estudiante con estos datos"}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsStudentOrAdmin])
def student_valoration_done_to_properties_api_view(request, id):

    student = Student.objects.filter(id=id).first()

    if student:

        aux = request.user.id == student.id

        if request.method == 'GET':
            
            if not (aux or request.user.isAdministrator):
                return Response({'message':"No puede acceder a las valoraciones de otro estudiante!"}, status=status.HTTP_403_FORBIDDEN)

            #queryset
        
            res = PropertyValoration.objects.filter(valuer=student)
            serializer = PropertyValorationSerializer(res, many=True)
            return Response(serializer.data, status = status.HTTP_200_OK)
    

    return Response({'message': "No se ha encontrado un estudiante con estos datos"}, status=status.HTTP_400_BAD_REQUEST) 



@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsStudent])
def student_verify_password(request):
    # Obtener la contraseña introducida por el usuario desde la solicitud
    entered_password = request.data.get('password')
    
    # Obtener el usuario y la contraseña encriptada almacenada en la base de datos
    user = Student.objects.get(username=request.user.username)
    stored_password = user.password
    
    # Verificar si las contraseñas coinciden
    if check_password(entered_password, stored_password):
        # Las contraseñas coinciden
        return Response({'password_correct': True}, status=status.HTTP_201_CREATED)
    else:
        return Response({'password_correct': False}, status=status.HTTP_201_CREATED)
    



@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsStudent])
def student_profile_change_password(request):

    new_password = request.data.get('new_password')

    if len(new_password) < 8:
        return Response({'message': 'La contraseña debe tener al menos 8 caracteres'}, status=status.HTTP_400_BAD_REQUEST)
        

    try:
        user = Student.objects.get(username=request.user.username)
        user.set_password(new_password)
        user.save()
        return Response({'message': 'Contraseña actualizada correctamente'}, status=status.HTTP_200_OK)
    except Student.DoesNotExist:
        return Response({'message': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    



@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsStudentOrAdmin])
def student_photo_update(request, id):
    student = Student.objects.filter(id=id).first()
    if student:
        aux = request.user.id == student.id
        if not (aux or request.user.isAdministrator):
            return Response({'message':"No puede actualizar la foto de otro estudiante!"}, status=status.HTTP_403_FORBIDDEN)
        data = request.data
        serializer = StudentUpdateSerializer(student, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({'message':"No se ha encontrado un estudiante con estos datos"}, status=status.HTTP_400_BAD_REQUEST)