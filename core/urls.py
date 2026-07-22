from django.urls import path

from . import views
from patients import web_views as patient_web_views
from triage import web_views as triage_web_views
from staff import web_views as staff_web_views

urlpatterns = [
    # Inicio
    path("", views.home, name="home"),
    path("login/", views.login_page, name="login"),
    path("logout/", views.logout_page, name="logout"),

    # Pacientes
    path("pacientes/", views.pacientes, name="pacientes"),
    path("pacientes/nuevo/", patient_web_views.paciente_crear, name="paciente_crear"),
    path("pacientes/<int:paciente_id>/", patient_web_views.paciente_detalle, name="paciente_detalle"),
    path("pacientes/<int:paciente_id>/editar/", patient_web_views.paciente_editar, name="paciente_editar"),
    path("pacientes/<int:paciente_id>/eliminar/", patient_web_views.paciente_eliminar, name="paciente_eliminar"),

    # Triaje
    path("triaje/", triage_web_views.triaje_lista, name="triaje"),
    path("triaje/nuevo/", triage_web_views.triaje_crear, name="triaje_crear"),
    path("triaje/<int:triaje_id>/", triage_web_views.triaje_detalle, name="triaje_detalle"),
    path("triaje/<int:triaje_id>/editar/", triage_web_views.triaje_editar, name="triaje_editar"),
    path("triaje/<int:triaje_id>/eliminar/", triage_web_views.triaje_eliminar, name="triaje_eliminar"),

    # Personal médico
    path("medicos/", staff_web_views.personal_lista, name="medicos"),
    path("medicos/nuevo/", staff_web_views.personal_crear, name="personal_crear"),
    path("medicos/<int:personal_id>/", staff_web_views.personal_detalle, name="personal_detalle"),
    path("medicos/<int:personal_id>/editar/", staff_web_views.personal_editar, name="personal_editar"),
    path("medicos/<int:personal_id>/eliminar/", staff_web_views.personal_eliminar, name="personal_eliminar"),

    # Usuarios
    path("usuarios/", views.usuarios, name="usuarios"),
]