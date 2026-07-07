from datetime import date
from rest_framework import serializers
from .models import Paciente, Tutor, AntecedenteMedico


class TutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutor
        fields = [
            'id',
            'paciente',
            'nombre_completo',
            'parentesco',
            'telefono',
            'es_principal',
        ]


class AntecedenteMedicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AntecedenteMedico
        fields = [
            'id',
            'paciente',
            'embarazo_complicado',
            'prematuro',
            'peso_nacimiento',
            'semanas_gestacion',
            'enfermedades_cronicas',
            'cirugias_previas',
            'vacunacion_al_dia',
            'hospitalizaciones_previas',
        ]
        read_only_fields = ['paciente']


class PacienteSerializer(serializers.ModelSerializer):
    edad = serializers.SerializerMethodField()
    tutores = TutorSerializer(many=True, read_only=True)
    antecedente_medico = AntecedenteMedicoSerializer(read_only=True)

    class Meta:
        model = Paciente
        fields = [
            'id',
            'historia_clinica',
            'nombre',
            'apellido',
            'fecha_nacimiento',
            'sexo',
            'nombre_tutor',
            'telefono_emergencia',
            'alergias',
            'edad',
            'tutores',
            'antecedente_medico',
            'created_at',
        ]
        read_only_fields = ['created_at']

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


class PacienteCreateUpdateSerializer(serializers.ModelSerializer):
    tutores = TutorSerializer(many=True, required=False)
    antecedente_medico = AntecedenteMedicoSerializer(required=False)

    class Meta:
        model = Paciente
        fields = [
            'id',
            'historia_clinica',
            'nombre',
            'apellido',
            'fecha_nacimiento',
            'sexo',
            'nombre_tutor',
            'telefono_emergencia',
            'alergias',
            'tutores',
            'antecedente_medico',
        ]

    def create(self, validated_data):
        tutores_data = validated_data.pop('tutores', [])
        antecedente_data = validated_data.pop('antecedente_medico', None)
        paciente = Paciente.objects.create(**validated_data)

        for tutor_data in tutores_data:
            Tutor.objects.create(paciente=paciente, **tutor_data)

        if antecedente_data:
            AntecedenteMedico.objects.create(paciente=paciente, **antecedente_data)

        return paciente

    def update(self, instance, validated_data):
        tutores_data = validated_data.pop('tutores', None)
        antecedente_data = validated_data.pop('antecedente_medico', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if tutores_data is not None:
            instance.tutores.all().delete()
            for tutor_data in tutores_data:
                Tutor.objects.create(paciente=instance, **tutor_data)

        if antecedente_data is not None:
            AntecedenteMedico.objects.filter(paciente=instance).delete()
            AntecedenteMedico.objects.create(paciente=instance, **antecedente_data)

        return instance


class PacienteListSerializer(serializers.ModelSerializer):
    edad = serializers.SerializerMethodField()
    tutor_principal = serializers.SerializerMethodField()

    class Meta:
        model = Paciente
        fields = [
            'id',
            'historia_clinica',
            'nombre',
            'apellido',
            'edad',
            'tutor_principal',
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

    def get_tutor_principal(self, obj):
        principal = obj.tutores.filter(es_principal=True).first()
        return principal.nombre_completo if principal else None
