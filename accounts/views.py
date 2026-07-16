from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, get_user_model

from .permissions import RolPermission
from .serializers import (
    UsuarioSerializer,
    UsuarioCreateSerializer,
    UsuarioUpdateSerializer,
    UsuarioListSerializer
)

Usuario = get_user_model()


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    permission_classes = [RolPermission]

    def get_serializer_class(self):
        if self.action == 'create':
            return UsuarioCreateSerializer
        if self.action in ['update', 'partial_update']:
            return UsuarioUpdateSerializer
        if self.action == 'list':
            return UsuarioListSerializer
        return UsuarioSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response(
            {'error': 'Username y password son requeridos'},
            status=HTTP_400_BAD_REQUEST
        )
    
    user = authenticate(username=username, password=password)
    
    if not user:
        return Response(
            {'error': 'Credenciales inválidas'},
            status=HTTP_400_BAD_REQUEST
        )
    
    token, _ = Token.objects.get_or_create(user=user)
    
    return Response(
        {
            'token': token.key,
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
        },
        status=HTTP_200_OK
    )
