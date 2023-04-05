from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status


from apis.models import Experience, Student
from .serializers import ExperienceSerializer


@api_view(['GET', 'POST'])
def experience_api_view(request):

    if request.method == 'GET':

        #queryset
        experiences = Experience.objects.all()
        serializer = ExperienceSerializer(experiences, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    #create
    elif request.method == 'POST':
        data = request.data
        serializer = ExperienceSerializer(data = data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from django.db import models
@api_view(['GET', 'PUT', 'DELETE'])
def experience_detail_api_view(request, id):
        
    # queryset
    experience = Experience.objects.filter(id=id).first()

    # validacion
    if experience:
        
        if request.method == 'GET':
            serializer = ExperienceSerializer(experience)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        elif request.method == 'PUT':
            data = request.data
            data['student'] = data['student']
            serializer = ExperienceSerializer(experience, data = data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        elif request.method == 'DELETE':
            experience.delete()
            return Response({'message':"Experiencia eliminada correctamente!"}, status=status.HTTP_200_OK)
        
    return Response({'message':"No se ha encontrado una experiencia con estos datos"}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def experience_student_api_view(request, id):

   student = Student.objects.filter(id=id).first()

   if student:
    
    if request.method == 'GET':
        all_experiences = Experience.objects.all()
        res = []

        for p in all_experiences:
            if p.student == student:
                res.append(p)
        
        serializer = ExperienceSerializer(res, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    return Response({'message': 'No se ha encontrado un estudiante con estos datos'}, status=status.HTTP_400_BAD_REQUEST)