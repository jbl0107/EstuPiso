from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework import status

from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from apis.permissions_decorators import IsStudentOrAdmin, IsStudent
from rest_framework.exceptions import PermissionDenied

from apis.models import StudentAnnouncement, Student
from .serializers import StudentAnnouncementSerializer


@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
def studentAnnouncement_api_view(request):

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
        studentAnnouncements = StudentAnnouncement.objects.all()
        serializer = StudentAnnouncementSerializer(studentAnnouncements, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    #create
    elif request.method == 'POST':
        data = request.data
        data['student'] = request.user.id
        serializer = StudentAnnouncementSerializer(data = data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([JWTAuthentication])
def studentAnnouncement_detail_api_view(request, id):


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
    studentAnnouncement = StudentAnnouncement.objects.filter(id=id).first()

    

    # validacion
    if studentAnnouncement:

        aux = request.user.id == studentAnnouncement.student.id

        if request.method == 'GET':
            serializer = StudentAnnouncementSerializer(studentAnnouncement)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        elif request.method == 'PUT':

            if not aux:
                return Response({'message':"No puede modificar un anuncio de estudiante que no le pertenece"}, status=status.HTTP_403_FORBIDDEN)
           
            data = request.data
            data['student'] = request.user.id
            serializer = StudentAnnouncementSerializer(studentAnnouncement, data = data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        elif request.method == 'DELETE':
             
            if not (aux or request.user.isAdministrator):
                return Response({'message':"No puede borrar un anuncio de estudiante que no le pertenece"}, status=status.HTTP_403_FORBIDDEN)
           
            studentAnnouncement.delete()
            return Response({'message':"Anuncio de estudiante eliminado correctamente!"}, status=status.HTTP_200_OK)
        
    return Response({'message':"No se ha encontrado un anuncio de estudiante con estos datos"}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsStudentOrAdmin])
def studentAnnouncement_student_api_view(request, id):
        
    # queryset
    student = Student.objects.filter(id=id).first()

    # validacion
    if student:
        
        if request.method == 'GET':
            all_announcements = StudentAnnouncement.objects.all()

            studentAnnouncement = None

            for a in all_announcements:
                if a.student == student:
                    studentAnnouncement = a
                    break

            serializer = StudentAnnouncementSerializer(studentAnnouncement)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
    return Response({'message':"No se ha encontrado un estudiante con estos datos"}, status=status.HTTP_400_BAD_REQUEST)
