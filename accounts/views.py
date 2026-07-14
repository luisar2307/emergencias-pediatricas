from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """
    Endpoint de login que retorna un token de autenticación.
    
    Parámetros:
    - username: nombre de usuario
    - password: contraseña
    
    Retorna:
    - token: token de autenticación
    - user_id: ID del usuario
    - username: nombre de usuario
    """
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
