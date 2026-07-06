from datetime import date
from rest_framework import serializers
from .models import Paciente


class PacienteSerializer(serializers.ModelSerializer):
    edad = serializers.SerializerMethodField()

    class Meta:
        model = Paciente
        fields = [
            "id",
            "historia_clinica",
            "nombre",
            "apellido",
            "fecha_nacimiento",
            "edad",
            "nombre_tutor",
            "telefono_emergencia",
        ]

    def get_edad(self, obj):
        today = date.today()
        return (
            today.year
            - obj.fecha_nacimiento.year
            - (
                (today.month, today.day)
                < (obj.fecha_nacimiento.month, obj.fecha_nacimiento.day)
            )
        )