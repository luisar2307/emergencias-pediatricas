from functools import wraps
import unicodedata

from django.contrib import messages
from django.shortcuts import redirect


def normalizar_rol(valor):
    """
    Convierte un rol a mayúsculas, elimina espacios,
    elimina acentos y unifica nombres equivalentes.
    """

    if not valor:
        return ""

    texto = str(valor).strip().upper()

    texto = unicodedata.normalize(
        "NFD",
        texto,
    )

    texto = "".join(
        caracter
        for caracter in texto
        if unicodedata.category(caracter) != "Mn"
    )

    equivalencias = {
        "ADMINISTRADOR": "ADMIN",
        "ADMINISTRACION": "ADMIN",
        "DOCTOR": "MEDICO",
        "DOCTORA": "MEDICO",
        "MEDICA": "MEDICO",
        "ENFERMERA": "ENFERMERO",
        "RECEPCIONISTA": "RECEPCION",
    }

    return equivalencias.get(texto, texto)


def obtener_rol_usuario(usuario):
    """
    Devuelve el rol del usuario.

    Todo superusuario de Django tendrá rol ADMIN.
    """

    if not usuario.is_authenticated:
        return ""

    if usuario.is_superuser:
        return "ADMIN"

    rol = getattr(usuario, "rol", "")

    if rol:
        return normalizar_rol(rol)

    grupo = usuario.groups.first()

    if grupo:
        return normalizar_rol(grupo.name)

    return "USUARIO"


def usuario_tiene_rol(usuario, roles_permitidos):
    """
    Verifica si el usuario tiene alguno de los roles permitidos.
    """

    if not usuario.is_authenticated:
        return False

    if usuario.is_superuser:
        return True

    rol_usuario = obtener_rol_usuario(usuario)

    roles_normalizados = [
        normalizar_rol(rol)
        for rol in roles_permitidos
    ]

    return rol_usuario in roles_normalizados


def permitir_roles(roles=None):
    """
    Decorador para restringir vistas por rol.

    Ejemplo:

    @permitir_roles(["ADMIN", "MEDICO"])
    """

    roles = roles or []

    def decorator(view_func):

        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            if not request.user.is_authenticated:
                return redirect("login")

            if usuario_tiene_rol(request.user, roles):
                return view_func(
                    request,
                    *args,
                    **kwargs,
                )

            messages.error(
                request,
                "No tienes permiso para acceder a esta sección."
            )

            return redirect("home")

        return wrapper

    return decorator