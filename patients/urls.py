from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PacienteViewSet, TutorViewSet
from triage import web_views as triage_web_views

router = DefaultRouter()
router.register(r'pacientes', PacienteViewSet, basename='paciente')
router.register(r'tutores', TutorViewSet, basename='tutor')

urlpatterns = [
    path('', include(router.urls)),
    path(
    "triaje/",
    triage_web_views.triaje_lista,
    name="triaje",
),
path(
    "triaje/nuevo/",
    triage_web_views.triaje_crear,
    name="triaje_crear",
),
path(
    "triaje/<int:triaje_id>/",
    triage_web_views.triaje_detalle,
    name="triaje_detalle",
),
path(
    "triaje/<int:triaje_id>/editar/",
    triage_web_views.triaje_editar,
    name="triaje_editar",
),
path(
    "triaje/<int:triaje_id>/eliminar/",
    triage_web_views.triaje_eliminar,
    name="triaje_eliminar",
),
]