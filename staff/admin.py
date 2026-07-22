from django.contrib import admin

from .models import PersonalMedico


@admin.register(PersonalMedico)
class PersonalMedicoAdmin(admin.ModelAdmin):
    list_display = (
        "nombre_completo",
        "especialidad",
        "registro_medico",
        "en_turno",
    )

    list_filter = (
        "en_turno",
        "especialidad",
    )

    search_fields = (
        "user__first_name",
        "user__last_name",
        "user__username",
        "user__email",
        "especialidad",
        "registro_medico",
    )

    list_editable = (
        "en_turno",
    )

    ordering = (
        "user__first_name",
        "user__last_name",
    )

    @admin.display(
        description="Nombre",
        ordering="user__first_name",
    )
    def nombre_completo(self, obj):
        return (
            obj.user.get_full_name()
            or obj.user.username
        )