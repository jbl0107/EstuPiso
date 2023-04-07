from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from apis.models import GroupReservation, Student
from .serializers import GroupReservationSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from apis.permissions_decorators import IsStudentOrAdmin



@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def groupReservation_api_view(request):

    if request.user.isAdministrator:
    
        if request.method == 'GET':

            #queryset
            groupReservations = GroupReservation.objects.all()
            serializer = GroupReservationSerializer(groupReservations, many=True)
            return Response(serializer.data, status = status.HTTP_200_OK)
    else:
        return Response({"message":"Debe ser administrador para obtener todas las solicitudes"}, status=status.HTTP_400_BAD_REQUEST)

    
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsStudentOrAdmin])
def groupReservation_post_api_view(request):

    #create
    if request.method == 'POST':

        data = request.data

        if int(data.get('student')) != request.user.id and request.user.isAdministrator == False:
            return Response({'message': 'No puede enviar una solicitud como otro estudiante'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = GroupReservationSerializer(data = data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET', 'DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsStudentOrAdmin])
def groupReservation_detail_api_view(request, id):
        
    # queryset
    groupReservation = GroupReservation.objects.filter(id=id).first()

    # validacion
    if groupReservation:
        
        if request.user.id == groupReservation.student.id or request.user.isAdministrator:

            if request.method == 'GET':
                serializer = GroupReservationSerializer(groupReservation)
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            
            elif request.method == 'DELETE':
                groupReservation.delete()
                return Response({'message':"Solicitud grupal eliminada correctamente!"}, status=status.HTTP_200_OK)
            
        else:
            return Response({'message':"No puede eliminar una solicitud que no le pertenece"}, status=status.HTTP_403_FORBIDDEN)
        
    return Response({'message':"No se ha encontrado una solicitud grupal con estos datos"}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsStudentOrAdmin])
def groupReservation_student_api_view(request, id):

   student = Student.objects.filter(id=id).first()

   if student:
    
    if request.user.id == id or request.user.isAdministrator:

        if request.method == 'GET':

            res = GroupReservation.objects.filter(student=student)
            serializer = GroupReservationSerializer(res, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Solo puede obtener todas sus solicitudes grupales'}, status=status.HTTP_400_BAD_REQUEST)
        
   else:
    return Response({'message': 'No se ha encontrado un estudiante con estos datos'}, status=status.HTTP_400_BAD_REQUEST)