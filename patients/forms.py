from django import forms

from .models import Paciente


class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente

        fields = [
            "historia_clinica",
            "nombre",
            "apellido",
            "fecha_nacimiento",
            "sexo",
            "nombre_tutor",
            "telefono_emergencia",
            "alergias",
        ]

        widgets = {
            "historia_clinica": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ejemplo: HC-0001",
                }
            ),
            "nombre": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nombres del paciente",
                }
            ),
            "apellido": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Apellidos del paciente",
                }
            ),
            "fecha_nacimiento": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),
            "sexo": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
            "nombre_tutor": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nombre del representante",
                }
            ),
            "telefono_emergencia": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Número de contacto",
                }
            ),
            "alergias": forms.Textarea(
                attrs={
                    "class": "form-control textarea",
                    "rows": 4,
                    "placeholder": (
                        "Registre alergias conocidas o escriba "
                        "'Ninguna'"
                    ),
                }
            ),
        }

        labels = {
            "historia_clinica": "Número de historia clínica",
            "nombre": "Nombres",
            "apellido": "Apellidos",
            "fecha_nacimiento": "Fecha de nacimiento",
            "sexo": "Sexo",
            "nombre_tutor": "Tutor o representante",
            "telefono_emergencia": "Teléfono de emergencia",
            "alergias": "Alergias conocidas",
        }

    def clean_historia_clinica(self):
        historia_clinica = self.cleaned_data[
            "historia_clinica"
        ].strip()

        existe = Paciente.objects.filter(
            historia_clinica__iexact=historia_clinica
        )

        if self.instance.pk:
            existe = existe.exclude(
                pk=self.instance.pk
            )

        if existe.exists():
            raise forms.ValidationError(
                "Ya existe un paciente con esa historia clínica."
            )

        return historia_clinica