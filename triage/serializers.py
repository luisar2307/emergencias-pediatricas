from rest_framework import serializers
from .models import Triaje
from patients.serializers import PacienteSerializer
from staff.serializers import PersonalMedicoSerializer


# Serializer para Escritura (POST, PUT) - Recibe IDs numéricos simples
class TriajeSerializer(serializers.ModelSerializer):
    nivel_urgencia = serializers.CharField(read_only=True)

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

    def validate(self, data):
        required_fields = [
            "frecuencia_cardiaca",
            "frecuencia_respiratoria",
            "temperatura",
            "saturacion_oxigeno",
        ]
        missing = [field for field in required_fields if field not in data or data[field] is None]
        if missing:
            raise serializers.ValidationError(
                {
                    "detail": (
                        "Los siguientes campos son requeridos para el triaje: "
                        + ", ".join(missing)
                    )
                }
            )

        temperatura = data["temperatura"]
        if temperatura < 30 or temperatura > 45:
            raise serializers.ValidationError(
                {"temperatura": "Temperatura fuera de rango válido (30.0 - 45.0)."}
            )

        frecuencia_cardiaca = data["frecuencia_cardiaca"]
        if frecuencia_cardiaca < 20 or frecuencia_cardiaca > 240:
            raise serializers.ValidationError(
                {"frecuencia_cardiaca": "Frecuencia cardíaca fuera de rango válido (20 - 240)."}
            )

        frecuencia_respiratoria = data["frecuencia_respiratoria"]
        if frecuencia_respiratoria < 5 or frecuencia_respiratoria > 60:
            raise serializers.ValidationError(
                {"frecuencia_respiratoria": "Frecuencia respiratoria fuera de rango válido (5 - 60)."}
            )

        saturacion = data["saturacion_oxigeno"]
        if saturacion < 50 or saturacion > 100:
            raise serializers.ValidationError(
                {"saturacion_oxigeno": "Saturación de oxígeno fuera de rango válido (50 - 100)."}
            )

        return data

    def create(self, validated_data):
        triaje = Triaje(**validated_data)
        triaje.nivel_urgencia = triaje.calcular_nivel_urgencia()
        triaje.save()
        return triaje

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.nivel_urgencia = instance.calcular_nivel_urgencia()
        instance.save()
        return instance


# Serializer para Lectura (GET) - Expone la información completa detallada
class TriajeDetalleSerializer(serializers.ModelSerializer):
    paciente = PacienteSerializer(read_only=True)
    personal = PersonalMedicoSerializer(read_only=True)

    class Meta:
        model = Triaje
        fields = "__all__"