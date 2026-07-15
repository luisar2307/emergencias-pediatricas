from django.db import models


class Paciente(models.Model):
    SEXO = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ]
    
    historia_clinica = models.CharField(max_length=64, unique=True, verbose_name='Historia Clínica')
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    apellido = models.CharField(max_length=100, verbose_name='Apellido')
    fecha_nacimiento = models.DateField(verbose_name='Fecha de Nacimiento')
    sexo = models.CharField(max_length=1, choices=SEXO, verbose_name='Sexo')
    nombre_tutor = models.CharField(max_length=150, blank=True, verbose_name='Nombre del Tutor')
    telefono_emergencia = models.CharField(max_length=32, blank=True, verbose_name='Teléfono de Emergencia')
    alergias = models.TextField(blank=True, verbose_name='Alergias')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Registro')

    class Meta:
        db_table = 'pacientes'
        ordering = ['-created_at']
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'

    def __str__(self):
        return f'{self.nombre} {self.apellido} ({self.historia_clinica})'

    def edad(self):
        from datetime import date
        hoy = date.today()
        return hoy.year - self.fecha_nacimiento.year - (
            (hoy.month, hoy.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day)
        )


class Tutor(models.Model):
    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        related_name='tutores',
        verbose_name='Paciente'
    )
    nombre_completo = models.CharField(max_length=200, verbose_name='Nombre Completo')
    parentesco = models.CharField(max_length=50, verbose_name='Parentesco')
    telefono = models.CharField(max_length=20, verbose_name='Teléfono')
    es_principal = models.BooleanField(default=False, verbose_name='Tutor Principal')

    class Meta:
        db_table = 'tutores'
        verbose_name = 'Tutor'
        verbose_name_plural = 'Tutores'

    def __str__(self):
        return f'{self.nombre_completo} ({self.parentesco})'


class AntecedenteMedico(models.Model):
    paciente = models.OneToOneField(
        Paciente,
        on_delete=models.CASCADE,
        related_name='antecedente_medico',
        verbose_name='Paciente'
    )
    embarazo_complicado = models.BooleanField(default=False, verbose_name='Embarazo Complicado')
    prematuro = models.BooleanField(default=False, verbose_name='Prematuro')
    peso_nacimiento = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Peso al Nacer (kg)'
    )
    semanas_gestacion = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name='Semanas de Gestación'
    )
    enfermedades_cronicas = models.TextField(blank=True, verbose_name='Enfermedades Crónicas')
    cirugias_previas = models.TextField(blank=True, verbose_name='Cirugías Previas')
    vacunacion_al_dia = models.BooleanField(default=False, verbose_name='Vacunación al Día')
    hospitalizaciones_previas = models.TextField(blank=True, verbose_name='Hospitalizaciones Previas')

    class Meta:
        db_table = 'antecedentes_medicos'
        verbose_name = 'Antecedente Médico'
        verbose_name_plural = 'Antecedentes Médicos'

    def __str__(self):
        return f'Antecedentes médicos de {self.paciente}'
    
