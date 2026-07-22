from datetime import date

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

        labels = {
            "historia_clinica": "Número de historia clínica",
            "nombre": "Nombres",
            "apellido": "Apellidos",
            "fecha_nacimiento": "Fecha de nacimiento",
            "sexo": "Sexo",
            "nombre_tutor": "Nombre del tutor o representante",
            "telefono_emergencia": "Teléfono de emergencia",
            "alergias": "Alergias conocidas",
        }

        widgets = {
            "historia_clinica": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ejemplo: HC-0001",
                    "autocomplete": "off",
                }
            ),
            "nombre": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nombres del paciente",
                    "autocomplete": "given-name",
                }
            ),
            "apellido": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Apellidos del paciente",
                    "autocomplete": "family-name",
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
                    "class": "form-control form-select",
                }
            ),
            "nombre_tutor": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nombre completo del representante",
                    "autocomplete": "name",
                }
            ),
            "telefono_emergencia": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ejemplo: 0991234567",
                    "autocomplete": "tel",
                    "inputmode": "tel",
                }
            ),
            "alergias": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": (
                        "Escriba las alergias conocidas. "
                        "Déjelo vacío si no presenta alergias."
                    ),
                    "rows": 4,
                }
            ),
        }

    def clean_fecha_nacimiento(self):
        fecha_nacimiento = self.cleaned_data.get("fecha_nacimiento")

        if fecha_nacimiento and fecha_nacimiento > date.today():
            raise forms.ValidationError(
                "La fecha de nacimiento no puede ser futura."
            )

        return fecha_nacimiento

    def clean_historia_clinica(self):
        historia_clinica = self.cleaned_data.get("historia_clinica")

        if historia_clinica:
            historia_clinica = historia_clinica.strip().upper()

        consulta = Paciente.objects.filter(
            historia_clinica__iexact=historia_clinica
        )

        if self.instance.pk:
            consulta = consulta.exclude(pk=self.instance.pk)

        if consulta.exists():
            raise forms.ValidationError(
                "Ya existe un paciente con esta historia clínica."
            )

        return historia_clinica

    def clean_telefono_emergencia(self):
        telefono = self.cleaned_data.get("telefono_emergencia", "").strip()

        if telefono:
            caracteres_permitidos = set(
                "0123456789+-() "
            )

            if not set(telefono).issubset(caracteres_permitidos):
                raise forms.ValidationError(
                    "El teléfono contiene caracteres no permitidos."
                )

        return telefono