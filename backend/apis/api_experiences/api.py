from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from apis.permissions_decorators import IsStudentOrAdmin, IsStudent

from apis.models import Experience, Student
from .serializers import ExperienceSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import PermissionDenied


@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
def experience_api_view(request):


    def check_permissions(request):

        if request.method == 'GET':
            for permission_class in [IsAuthenticated, IsStudentOrAdmin]:
                permission = permission_class()
                if not permission.has_permission(request, None):
                    raise PermissionDenied(getattr(permission, 'message', None))

        if request.method == 'POST':
            for permission_class in [IsAuthenticated, IsStudent]:
                permission = permission_class()
                if not permission.has_permission(request, None):
                    raise PermissionDenied(getattr(permission, 'message', None))

    check_permissions(request)


    if request.method == 'GET':

        #queryset
        experiences = Experience.objects.all()
        serializer = ExperienceSerializer(experiences, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    #create
    elif request.method == 'POST':
        data = request.data
        data['student'] = request.user.id
        if int(data.get('student')) != request.user.id:
            return Response({'message': 'No puede crear una experiencia para otro estudiante'}, status=status.HTTP_403_FORBIDDEN) 

        serializer = ExperienceSerializer(data = data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([JWTAuthentication])
def experience_detail_api_view(request, id):

    def check_permissions(request):

        if request.method == 'GET':
            for permission_class in [IsAuthenticated, IsStudentOrAdmin]:
                permission = permission_class()
                if not permission.has_permission(request, None):
                    raise PermissionDenied(getattr(permission, 'message', None))

        if request.method == 'PUT':
            for permission_class in [IsAuthenticated, IsStudent]:
                permission = permission_class()
                if not permission.has_permission(request, None):
                    raise PermissionDenied(getattr(permission, 'message', None))
                
        elif request.method == 'DELETE':
            for permission_class in [IsAuthenticated, IsStudentOrAdmin]:
                permission = permission_class()
                if not permission.has_permission(request, None):
                    raise PermissionDenied(getattr(permission, 'message', None))

    check_permissions(request)
        
    # queryset
    experience = Experience.objects.filter(id=id).first()

    # validacion
    if experience:
        
        if request.method == 'GET':
            serializer = ExperienceSerializer(experience)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        
            
        if request.method == 'PUT':

            if request.user.id != experience.student.id:
                 return Response({'message':"No puede actualizar una experiencia que no le pertenece"}, status=status.HTTP_403_FORBIDDEN)

            data = request.data
            data['student'] = request.user.id
            serializer = ExperienceSerializer(experience, data = data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        elif request.method == 'DELETE':
            if request.user.id != experience.student.id and not request.user.isAdministrator:
                return Response({'message':"No puede eliminar una experiencia que no le pertenece"}, status=status.HTTP_403_FORBIDDEN)
           
            experience.delete()
            return Response({'message':"Experiencia eliminada correctamente!"}, status=status.HTTP_200_OK)
                
            
        
    return Response({'message':"No se ha encontrado una experiencia con estos datos"}, status=status.HTTP_404_NOT_FOUND)



@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsStudentOrAdmin])
def experience_student_api_view(request, id):

   student = Student.objects.filter(id=id).first()

   if student:
    
    if request.user.id == id or request.user.isAdministrator:

        if request.method == 'GET':
            
            experiences = Experience.objects.filter(student=student)
            serializer = ExperienceSerializer(experiences, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Solo puede obtener todas sus experiencias'}, status=status.HTTP_403_FORBIDDEN)

   else:

    return Response({'message': 'No se ha encontrado un estudiante con estos datos'}, status=status.HTTP_404_NOT_FOUND)