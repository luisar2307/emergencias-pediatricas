from rest_framework import serializers
from .models import Triaje
from patients.serializers import PacienteSerializer
from staff.serializers import PersonalMedicoSerializer


# Serializer para Escritura (POST, PUT) - Recibe IDs numéricos simples
class TriajeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Triaje
        fields = [
            "id",
            "paciente",
            "personal",
            "frecuencia_cardiaca",
            "frecuencia_respiratoria",
            "temperatura",
            "saturacion_oxigeno",
            "nivel_urgencia",
            "fecha_registro",
        ]


# Serializer para Lectura (GET) - Expone la información completa detallada
class TriajeDetalleSerializer(serializers.ModelSerializer):
    paciente = PacienteSerializer(read_only=True)
    personal = PersonalMedicoSerializer(read_only=True)

    class Meta:
        model = Triaje
        fields = "__all__"