from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication


# El objetivo de esta clase es, una vez que el usuario cierre sesión, el último token de refresh generado es también agregado a la
# black list 
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class LogoutView(TokenViewBase):


    def post(self, request):

        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message':"Sesión cerrada correctamente!"}, status=status.HTTP_205_RESET_CONTENT)
        
        except InvalidToken:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
