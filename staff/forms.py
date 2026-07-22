from django import forms
from django.contrib.auth import get_user_model

from .models import PersonalMedico


User = get_user_model()


class PersonalMedicoForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset=User.objects.all().order_by(
            "first_name",
            "last_name",
            "username",
        ),
        label="Usuario",
        empty_label="Seleccione un usuario",
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        ),
    )

    class Meta:
        model = PersonalMedico

        fields = [
            "user",
            "especialidad",
            "registro_medico",
            "en_turno",
        ]

        labels = {
            "especialidad": "Especialidad",
            "registro_medico": "Registro médico",
            "en_turno": "Actualmente en turno",
        }

        widgets = {
            "especialidad": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ejemplo: Pediatría",
                }
            ),
            "registro_medico": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ejemplo: MED-2026-001",
                }
            ),
            "en_turno": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }

    def clean_registro_medico(self):
        registro_medico = self.cleaned_data.get(
            "registro_medico",
            "",
        ).strip()

        if not registro_medico:
            return registro_medico

        registros = PersonalMedico.objects.filter(
            registro_medico__iexact=registro_medico
        )

        if self.instance.pk:
            registros = registros.exclude(
                pk=self.instance.pk
            )

        if registros.exists():
            raise forms.ValidationError(
                "Ya existe un miembro del personal con este registro médico."
            )

        return registro_medico