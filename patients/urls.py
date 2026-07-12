from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PacienteViewSet, TutorViewSet

router = DefaultRouter()
router.register(r'pacientes', PacienteViewSet, basename='paciente')
router.register(r'tutores', TutorViewSet, basename='tutor')

urlpatterns = [
    path('', include(router.urls)),
]