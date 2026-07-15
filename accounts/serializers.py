from rest_framework import serializers
from django.contrib.auth import get_user_model

Usuario = get_user_model()


class UsuarioSerializer(serializers.ModelSerializer):
    rol_display = serializers.CharField(source='get_rol_display', read_only=True)
    nombre_completo = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = Usuario
        fields = [
            'id', 
            'username', 
            'email', 
            'first_name', 
            'last_name',
            'nombre_completo',
            'rol', 
            'rol_display', 
            'telefono',
            'cedula_profesional', 
            'is_staff', 
            'is_active', 
            'date_joined'
        ]
        read_only_fields = ['date_joined']


class UsuarioCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = Usuario
        fields = [
            'username', 
            'email', 
            'password', 
            'password_confirm',
            'first_name', 
            'last_name', 
            'rol', 
            'telefono',
            'cedula_profesional', 
            'is_staff'
        ]

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({'password_confirm': 'Las contraseñas no coinciden.'})
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        return Usuario.objects.create_user(**validated_data)


class UsuarioUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = [
            'id', 
            'username', 
            'email', 
            'first_name', 
            'last_name',
            'rol', 
            'telefono', 
            'cedula_profesional', 
            'is_staff', 
            'is_active'
        ]


class UsuarioListSerializer(serializers.ModelSerializer):
    rol_display = serializers.CharField(source='get_rol_display', read_only=True)
    nombre_completo = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = Usuario
        fields = ['id', 
                  'username', 
                  'nombre_completo', 
                  'email', 
                  'rol', 
                  'rol_display', 
                  'is_active'
        ]