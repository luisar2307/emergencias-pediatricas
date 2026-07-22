from django import forms

from .models import Triaje


class TriajeForm(forms.ModelForm):
    class Meta:
        model = Triaje

        fields = [
            "paciente",
            "personal",
            "frecuencia_cardiaca",
            "frecuencia_respiratoria",
            "temperatura",
            "saturacion_oxigeno",
        ]

        labels = {
            "paciente": "Paciente",
            "personal": "Personal médico",
            "frecuencia_cardiaca": "Frecuencia cardíaca",
            "frecuencia_respiratoria": "Frecuencia respiratoria",
            "temperatura": "Temperatura",
            "saturacion_oxigeno": "Saturación de oxígeno",
        }

        widgets = {
            "paciente": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
            "personal": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
            "frecuencia_cardiaca": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ejemplo: 110",
                    "min": "1",
                }
            ),
            "frecuencia_respiratoria": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ejemplo: 24",
                    "min": "1",
                }
            ),
            "temperatura": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ejemplo: 37.5",
                    "step": "0.1",
                    "min": "30",
                    "max": "45",
                }
            ),
            "saturacion_oxigeno": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ejemplo: 98",
                    "min": "1",
                    "max": "100",
                }
            ),
        }

    def clean_frecuencia_cardiaca(self):
        valor = self.cleaned_data.get("frecuencia_cardiaca")

        if valor is not None and valor > 300:
            raise forms.ValidationError(
                "La frecuencia cardíaca no puede superar 300."
            )

        return valor

    def clean_frecuencia_respiratoria(self):
        valor = self.cleaned_data.get("frecuencia_respiratoria")

        if valor is not None and valor > 150:
            raise forms.ValidationError(
                "La frecuencia respiratoria no puede superar 150."
            )

        return valor

    def clean_temperatura(self):
        valor = self.cleaned_data.get("temperatura")

        if valor is not None and (valor < 30 or valor > 45):
            raise forms.ValidationError(
                "La temperatura debe estar entre 30 y 45 °C."
            )

        return valor

    def clean_saturacion_oxigeno(self):
        valor = self.cleaned_data.get("saturacion_oxigeno")

        if valor is not None and (valor < 1 or valor > 100):
            raise forms.ValidationError(
                "La saturación debe estar entre 1 y 100 %."
            )

        return valor