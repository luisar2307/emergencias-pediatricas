from django.contrib import admin
from .models import Paciente, Tutor, AntecedenteMedico


class TutorInline(admin.TabularInline):
    model = Tutor
    extra = 1


class AntecedenteMedicoInline(admin.StackedInline):
    model = AntecedenteMedico
    extra = 0


@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ['historia_clinica', 'nombre', 'apellido', 'fecha_nacimiento', 'sexo', 'created_at']
    list_filter = ['sexo', 'created_at']
    search_fields = ['historia_clinica', 'nombre', 'apellido', 'nombre_tutor']
    inlines = [TutorInline, AntecedenteMedicoInline]


@admin.register(Tutor)
class TutorAdmin(admin.ModelAdmin):
    list_display = ['nombre_completo', 'parentesco', 'paciente', 'es_principal']
    list_filter = ['es_principal']
    search_fields = ['nombre_completo', 'paciente__nombre', 'paciente__apellido']


@admin.register(AntecedenteMedico)
class AntecedenteMedicoAdmin(admin.ModelAdmin):
    list_display = ['paciente', 'prematuro', 'vacunacion_al_dia']
    list_filter = ['prematuro', 'vacunacion_al_dia']