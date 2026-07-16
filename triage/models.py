from django.db import models
from django.utils import timezone


class Triaje(models.Model):
    URGENCIA_CRITICO = "critico"
    URGENCIA_URGENTE = "urgente"
    URGENCIA_MODERADO = "moderado"
    URGENCIA_NORMAL = "normal"

    URGENCIA_CHOICES = [
        (URGENCIA_CRITICO, "Crítico"),
        (URGENCIA_URGENTE, "Urgente"),
        (URGENCIA_MODERADO, "Moderado"),
        (URGENCIA_NORMAL, "Normal"),
    ]

    paciente = models.ForeignKey("patients.Paciente", on_delete=models.CASCADE)
    personal = models.ForeignKey("staff.PersonalMedico", on_delete=models.SET_NULL, null=True)
    frecuencia_cardiaca = models.PositiveIntegerField(null=True, blank=True)
    frecuencia_respiratoria = models.PositiveIntegerField(null=True, blank=True)
    temperatura = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    saturacion_oxigeno = models.PositiveIntegerField(null=True, blank=True)
    nivel_urgencia = models.CharField(max_length=32, choices=URGENCIA_CHOICES, blank=True)
    fecha_registro = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Triaje {self.id} - {self.paciente} - {self.nivel_urgencia}"

    def calcular_nivel_urgencia(self):
        """Calcula el nivel de urgencia según signos vitales."""
        if self.frecuencia_cardiaca is not None:
            if self.frecuencia_cardiaca > 180 or self.frecuencia_cardiaca < 60:
                return self.URGENCIA_CRITICO
        if self.frecuencia_respiratoria is not None:
            if self.frecuencia_respiratoria > 40:
                return self.URGENCIA_CRITICO
        if self.temperatura is not None:
            if self.temperatura >= 40.0 or self.temperatura <= 35.0:
                return self.URGENCIA_CRITICO
        if self.saturacion_oxigeno is not None:
            if self.saturacion_oxigeno < 90:
                return self.URGENCIA_CRITICO

        if self.frecuencia_cardiaca is not None:
            if self.frecuencia_cardiaca >= 140:
                return self.URGENCIA_URGENTE
        if self.frecuencia_respiratoria is not None:
            if self.frecuencia_respiratoria >= 31:
                return self.URGENCIA_URGENTE
        if self.temperatura is not None:
            if self.temperatura >= 39.0:
                return self.URGENCIA_URGENTE
        if self.saturacion_oxigeno is not None:
            if self.saturacion_oxigeno < 94:
                return self.URGENCIA_URGENTE

        if self.frecuencia_cardiaca is not None:
            if self.frecuencia_cardiaca >= 120:
                return self.URGENCIA_MODERADO
        if self.frecuencia_respiratoria is not None:
            if self.frecuencia_respiratoria >= 26:
                return self.URGENCIA_MODERADO
        if self.temperatura is not None:
            if self.temperatura >= 38.0:
                return self.URGENCIA_MODERADO
        if self.saturacion_oxigeno is not None:
            if self.saturacion_oxigeno < 96:
                return self.URGENCIA_MODERADO

        return self.URGENCIA_NORMAL

    def save(self, *args, **kwargs):
        self.nivel_urgencia = self.calcular_nivel_urgencia()
        super().save(*args, **kwargs)
