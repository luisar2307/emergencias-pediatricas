from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
	"""Custom user model minimal implementation to satisfy AUTH_USER_MODEL"""

	def __str__(self):
		return self.get_username()
