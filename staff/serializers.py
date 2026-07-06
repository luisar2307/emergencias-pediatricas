from django.contrib.auth.models import User
from rest_framework import serializers
from .models import PersonalMedico


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email"]


class PersonalMedicoSerializer(serializers.ModelSerializer):
    # Permite ver la información del usuario del sistema anidada
    usuario_detalles = UserSerializer(source="user", read_only=True)

    class Meta:
        model = PersonalMedico
        fields = [
            "id",
            "user",
            "usuario_detalles",
            "especialidad",
            "registro_medico",
            "en_turno",
        ]