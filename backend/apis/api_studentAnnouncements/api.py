from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status


from apis.models import StudentAnnouncement, Student
from .serializers import StudentAnnouncementSerializer


@api_view(['GET', 'POST'])
def studentAnnouncement_api_view(request):

    if request.method == 'GET':
        #queryset
        studentAnnouncements = StudentAnnouncement.objects.all()
        serializer = StudentAnnouncementSerializer(studentAnnouncements, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    #create
    elif request.method == 'POST':
        data = request.data
        serializer = StudentAnnouncementSerializer(data = data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET', 'PUT', 'DELETE'])
def studentAnnouncement_detail_api_view(request, id):
        
    # queryset
    studentAnnouncement = StudentAnnouncement.objects.filter(id=id).first()

    # validacion
    if studentAnnouncement:
        
        if request.method == 'GET':
            serializer = StudentAnnouncementSerializer(studentAnnouncement)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        elif request.method == 'PUT':
            data = request.data
            serializer = StudentAnnouncementSerializer(studentAnnouncement, data = data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        elif request.method == 'DELETE':
            studentAnnouncement.delete()
            return Response({'message':"Anuncio de estudiante eliminado correctamente!"}, status=status.HTTP_200_OK)
        
    return Response({'message':"No se ha encontrado un anuncio de estudiante con estos datos"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
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
