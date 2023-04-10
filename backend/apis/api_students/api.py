from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework import status

from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from apis.permissions_decorators import IsStudentOrAdmin, IsAdmin
from rest_framework.exceptions import PermissionDenied

from apis.models import Student, PropertyValoration
from .serializers import StudentSerializer
from apis.api_valoration.serializers import PropertyValorationSerializer



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
            serializer = StudentSerializer(student, data = data)
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
            '''
            valorations = PropertyValoration.objects.all()
            res = []
            
            for v in valorations:
                if v.valuer == student:
                    res.append(v)
            '''
            res = PropertyValoration.objects.filter(valuer=student)
            serializer = PropertyValorationSerializer(res, many=True)
            return Response(serializer.data, status = status.HTTP_200_OK)
    

    return Response({'message': "No se ha encontrado un estudiante con estos datos"}, status=status.HTTP_400_BAD_REQUEST) 