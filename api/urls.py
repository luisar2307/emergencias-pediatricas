from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Import viewsets from apps
from staff.views import PersonalMedicoViewSet
from patients.views import PacienteViewSet
from triage.views import TriajeViewSet
<<<<<<< HEAD
from accounts.views import UsuarioViewSet
=======
from accounts.views import login
>>>>>>> 48e53ad4fedd972c45de01646c3dcd5c2243b8da

router = DefaultRouter()
router.register(r"medicos", PersonalMedicoViewSet, basename="personal-medico")
router.register(r"registro", PacienteViewSet, basename="pacientes")
router.register(r"evaluacion", TriajeViewSet, basename="triajes")
router.register(r"usuarios", UsuarioViewSet, basename="usuario")
urlpatterns = [
    path("login", login, name="login"),
    path("", include(router.urls)),
]