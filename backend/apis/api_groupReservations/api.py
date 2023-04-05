from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status


from apis.models import GroupReservation, Student
from .serializers import GroupReservationSerializer


@api_view(['GET', 'POST'])
def groupReservation_api_view(request):

    if request.method == 'GET':

        #queryset
        groupReservations = GroupReservation.objects.all()
        serializer = GroupReservationSerializer(groupReservations, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    #create
    elif request.method == 'POST':
        data = request.data
        serializer = GroupReservationSerializer(data = data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET', 'DELETE'])
def groupReservation_detail_api_view(request, id):
        
    # queryset
    groupReservation = GroupReservation.objects.filter(id=id).first()

    # validacion
    if groupReservation:
        
        if request.method == 'GET':
            serializer = GroupReservationSerializer(groupReservation)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        
        elif request.method == 'DELETE':
            groupReservation.delete()
            return Response({'message':"Solicitud grupal eliminada correctamente!"}, status=status.HTTP_200_OK)
        
    return Response({'message':"No se ha encontrado una solicitud grupal con estos datos"}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def groupReservation_student_api_view(request, id):

   student = Student.objects.filter(id=id).first()

   if student:
    
    if request.method == 'GET':
        all_group = GroupReservation.objects.all()
        res = []

        for p in all_group:
            if p.student == student:
                res.append(p)
        
        serializer = GroupReservationSerializer(res, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    return Response({'message': 'No se ha encontrado un estudiante con estos datos'}, status=status.HTTP_400_BAD_REQUEST)