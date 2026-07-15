from django.urls import path, include
from rest_framework.routers import DefaultRouter
from accounts.views import UsuarioViewSet, login
# Import viewsets from apps
from staff.views import PersonalMedicoViewSet
from patients.views import PacienteViewSet
from triage.views import TriajeViewSet
from accounts.views import UsuarioViewSet

router = DefaultRouter()
router.register(r"medicos", PersonalMedicoViewSet, basename="personal-medico")
router.register(r"registro", PacienteViewSet, basename="pacientes")
router.register(r"evaluacion", TriajeViewSet, basename="triajes")
router.register(r"usuarios", UsuarioViewSet, basename="usuario")
urlpatterns = [
    path("login", login, name="login"),
    path("", include(router.urls)),
]