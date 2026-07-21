from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    ROLES = [
        ('medico', 'Médico Pediatra'),
        ('enfermero', 'Enfermero'),
        ('recepcion', 'Recepción'),
        ('admin', 'Administrador'),
    ]

    rol = models.CharField(
        max_length=20,
        choices=ROLES,
        default='recepcion',
        verbose_name='Rol'
    )
    telefono = models.CharField(max_length=20, blank=True, verbose_name='Teléfono')
    cedula_profesional = models.CharField(max_length=20, blank=True, verbose_name='Cédula Profesional')

    REQUIRED_FIELDS = ['email', 'rol']

    class Meta:
        db_table = 'usuarios'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return f'{self.get_full_name()} ({self.get_rol_display()})'

    def es_medico(self):
        return self.rol == 'medico'

    def es_enfermero(self):
        return self.rol == 'enfermero'

    def es_recepcion(self):
        return self.rol == 'recepcion'

    def es_admin(self):
        return self.rol == 'admin'