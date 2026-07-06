from django.db import models
from django.conf import settings


class PersonalMedico(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    especialidad = models.CharField(max_length=128, blank=True)
    registro_medico = models.CharField(max_length=64, blank=True)
    en_turno = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.especialidad}"
