from django.db import models


class Paciente(models.Model):
    historia_clinica = models.CharField(max_length=64, unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    nombre_tutor = models.CharField(max_length=150, blank=True)
    telefono_emergencia = models.CharField(max_length=32, blank=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.historia_clinica})"
