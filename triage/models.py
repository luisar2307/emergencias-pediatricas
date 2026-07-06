from django.db import models
from django.utils import timezone


class Triaje(models.Model):
    paciente = models.ForeignKey("patients.Paciente", on_delete=models.CASCADE)
    personal = models.ForeignKey("staff.PersonalMedico", on_delete=models.SET_NULL, null=True)
    frecuencia_cardiaca = models.PositiveIntegerField(null=True, blank=True)
    frecuencia_respiratoria = models.PositiveIntegerField(null=True, blank=True)
    temperatura = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    saturacion_oxigeno = models.PositiveIntegerField(null=True, blank=True)
    nivel_urgencia = models.CharField(max_length=32, blank=True)
    fecha_registro = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Triaje {self.id} - {self.paciente} - {self.nivel_urgencia}"
