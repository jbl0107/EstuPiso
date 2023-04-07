from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from apis.models import Student, PropertyValoration
from .serializers import StudentSerializer
from apis.api_valoration.serializers import PropertyValorationSerializer



@api_view(['GET', 'POST'])
def student_api_view(request):

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
def student_detail_api_view(request, id):
        
    # queryset
    student = Student.objects.filter(id=id).first()

    # validacion
    if student:
        
        if request.method == 'GET':
            serializer = StudentSerializer(student)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        elif request.method == 'PUT':
            data = request.data
            serializer = StudentSerializer(student, data = data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        elif request.method == 'DELETE':
            student.delete()
            return Response({'message':"Estudiante eliminado correctamente!"}, status=status.HTTP_200_OK)
        
    return Response({'message':"No se ha encontrado un estudiante con estos datos"}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def student_valoration_done_to_properties_api_view(request, id):

    student = Student.objects.filter(id=id).first()

    if student:

        if request.method == 'GET':

            #queryset
            valorations = PropertyValoration.objects.all()
            res = []
            
            for v in valorations:
                if v.valuer == student:
                    res.append(v)

            serializer = PropertyValorationSerializer(res, many=True)
            return Response(serializer.data, status = status.HTTP_200_OK)
    

    return Response({'message': "No se ha encontrado un estudiante con estos datos"}, status=status.HTTP_400_BAD_REQUEST) 