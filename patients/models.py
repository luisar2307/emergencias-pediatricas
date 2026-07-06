from django.db import models

class Paciente (models.Model):
    sexo = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ]

nombres = models.CharField(max_length=100, verbose_name= 'Nombres')
