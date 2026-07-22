from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone

from patients.models import Paciente


def obtener_contexto_base(usuario):
    """
    Genera la información del usuario, rol y permisos
    que se utiliza en el menú del sistema.
    """

    rol = "USUARIO"

    # Intenta obtener el rol desde diferentes estructuras posibles
    if hasattr(usuario, "rol") and usuario.rol:
        rol = str(usuario.rol).upper()

    elif hasattr(usuario, "perfil"):
        perfil = usuario.perfil

        if hasattr(perfil, "rol") and perfil.rol:
            rol = str(perfil.rol).upper()

    elif hasattr(usuario, "profile"):
        perfil = usuario.profile

        if hasattr(perfil, "rol") and perfil.rol:
            rol = str(perfil.rol).upper()

    elif usuario.is_superuser:
        rol = "ADMINISTRADOR"

    elif usuario.is_staff:
        rol = "PERSONAL MÉDICO"

    permisos = {
        "pacientes": True,
        "triaje": True,
        "emergencias": True,
        "historias": True,
        "medicos": True,
        "usuarios": usuario.is_superuser or usuario.is_staff,

        "crear_paciente": True,
        "ver_paciente": True,
        "editar_paciente": True,
        "eliminar_paciente": usuario.is_superuser or usuario.is_staff,
    }

    # El administrador tiene acceso completo
    if usuario.is_superuser:
        permisos = {
            "pacientes": True,
            "triaje": True,
            "emergencias": True,
            "historias": True,
            "medicos": True,
            "usuarios": True,

            "crear_paciente": True,
            "ver_paciente": True,
            "editar_paciente": True,
            "eliminar_paciente": True,
        }

    return {
        "usuario": usuario,
        "rol": rol,
        "permisos": permisos,
    }


def login_page(request):
    """
    Vista para iniciar sesión.
    """

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        if not username or not password:
            messages.error(
                request,
                "Ingrese su usuario y contraseña.",
            )

            return render(
                request,
                "core/login.html",
            )

        usuario = authenticate(
            request,
            username=username,
            password=password,
        )

        if usuario is not None:
            login(request, usuario)

            messages.success(
                request,
                f"Bienvenido, {usuario.get_full_name() or usuario.username}.",
            )

            next_url = request.GET.get("next")

            if next_url:
                return redirect(next_url)

            return redirect("home")

        messages.error(
            request,
            "El usuario o la contraseña son incorrectos.",
        )

    return render(
        request,
        "core/login.html",
    )


@login_required
def logout_page(request):
    """
    Cierra la sesión del usuario.
    """

    logout(request)

    messages.success(
        request,
        "La sesión se cerró correctamente.",
    )

    return redirect("login")


@login_required
def home(request):
    """
    Pantalla principal del sistema.
    """

    contexto = obtener_contexto_base(request.user)

    total_pacientes = Paciente.objects.count()

    pacientes_hoy = Paciente.objects.filter(
        created_at__date=timezone.localdate()
    ).count()

    pacientes_recientes = Paciente.objects.all().order_by(
        "-created_at"
    )[:5]

    contexto.update(
        {
            "total_pacientes": total_pacientes,
            "pacientes_hoy": pacientes_hoy,
            "pacientes_recientes": pacientes_recientes,
        }
    )

    return render(
        request,
        "core/home.html",
        contexto,
    )


@login_required
def pacientes(request):
    """
    Lista y estadísticas de pacientes.
    """

    pacientes_lista = Paciente.objects.all().order_by(
        "-created_at"
    )

    total_pacientes = pacientes_lista.count()

    pacientes_hoy = pacientes_lista.filter(
        created_at__date=timezone.localdate()
    ).count()

    total_masculinos = pacientes_lista.filter(
        sexo="M"
    ).count()

    total_femeninos = pacientes_lista.filter(
        sexo="F"
    ).count()

    contexto = obtener_contexto_base(request.user)

    contexto.update(
        {
            "pacientes_lista": pacientes_lista,
            "total_pacientes": total_pacientes,
            "pacientes_hoy": pacientes_hoy,
            "total_masculinos": total_masculinos,
            "total_femeninos": total_femeninos,
        }
    )

    return render(
        request,
        "core/pacientes.html",
        contexto,
    )


@login_required
def triaje(request):
    """
    Pantalla del módulo de triaje.
    """

    contexto = obtener_contexto_base(request.user)

    contexto.update(
        {
            "titulo": "Triaje pediátrico",
            "descripcion": (
                "Evaluación y clasificación inicial "
                "de los pacientes."
            ),
        }
    )

    return render(
        request,
        "core/triaje.html",
        contexto,
    )



@login_required
def medicos(request):
    """
    Pantalla del módulo de médicos.
    """

    contexto = obtener_contexto_base(request.user)

    contexto.update(
        {
            "titulo": "Médicos",
            "descripcion": (
                "Administración del personal médico."
            ),
        }
    )

    return render(
        request,
        "core/medicos.html",
        contexto,
    )


@login_required
def usuarios(request):
    """
    Pantalla del módulo de usuarios.
    """

    contexto = obtener_contexto_base(request.user)

    if not contexto["permisos"]["usuarios"]:
        messages.error(
            request,
            "No tiene permisos para acceder al módulo de usuarios.",
        )

        return redirect("home")

    contexto.update(
        {
            "titulo": "Usuarios",
            "descripcion": (
                "Administración de usuarios, roles y permisos."
            ),
        }
    )

    return render(
        request,
        "core/usuarios.html",
        contexto,
    )