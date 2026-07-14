from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Import viewsets from apps
from staff.views import PersonalMedicoViewSet
from patients.views import PacienteViewSet
from triage.views import TriajeViewSet
from accounts.views import login

router = DefaultRouter()
router.register(r"medicos", PersonalMedicoViewSet, basename="personal-medico")
router.register(r"registro", PacienteViewSet, basename="pacientes")
router.register(r"evaluacion", TriajeViewSet, basename="triajes")

urlpatterns = [
    path("login", login, name="login"),
    path("", include(router.urls)),
]