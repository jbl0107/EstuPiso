from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes
from rest_framework import status

from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from apis.permissions_decorators import IsAdmin
from rest_framework.exceptions import PermissionDenied
from rest_framework.exceptions import NotAuthenticated


from apis.models import Rule
from .serializers import RuleSerializer


@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
def rule_api_view(request):

    def check_permissions(request):
        if request.method == 'POST':
            if 'HTTP_AUTHORIZATION' not in request.META:
                raise NotAuthenticated()
            for permission_class in [IsAuthenticated, IsAdmin]:
                permission = permission_class()
                if not permission.has_permission(request, None):
                    raise PermissionDenied(getattr(permission, 'message', None))
                
    
    check_permissions(request)

    if request.method == 'GET':

        #queryset
        rules = Rule.objects.all()
        serializer = RuleSerializer(rules, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    #create
    elif request.method == 'POST':
        data = request.data
        serializer = RuleSerializer(data = data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([JWTAuthentication])
def rule_detail_api_view(request, id):

    def check_permissions(request):
        if request.method == 'PUT':
            if 'HTTP_AUTHORIZATION' not in request.META:
                raise NotAuthenticated()
            for permission_class in [IsAuthenticated, IsAdmin]:
                permission = permission_class()
                if not permission.has_permission(request, None):
                    raise PermissionDenied(getattr(permission, 'message', None))
                
        elif request.method == 'DELETE':
            if 'HTTP_AUTHORIZATION' not in request.META:
                raise NotAuthenticated()
            for permission_class in [IsAuthenticated, IsAdmin]:
                permission = permission_class()
                if not permission.has_permission(request, None):
                    raise PermissionDenied(getattr(permission, 'message', None))
                
    
    check_permissions(request)
    
        
    # queryset
    rule = Rule.objects.filter(id=id).first()

    # validacion
    if rule:
        
        if request.method == 'GET':
            serializer = RuleSerializer(rule)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        elif request.method == 'PUT':
            data = request.data
            serializer = RuleSerializer(rule, data = data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        elif request.method == 'DELETE':
            rule.delete()
            return Response({'message':"Norma eliminada correctamente!"}, status=status.HTTP_200_OK)
        
    return Response({'message':"No se ha encontrado una norma con estos datos"}, status=status.HTTP_404_NOT_FOUND)
