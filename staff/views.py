# views/staff.py
from rest_framework import viewsets
from .models import PersonalMedico
from .serializers import PersonalMedicoSerializer
from accounts.permissions import RolPermission


class PersonalMedicoViewSet(viewsets.ModelViewSet):
    queryset = PersonalMedico.objects.all().select_related("user")
    serializer_class = PersonalMedicoSerializer
    permission_classes = [RolPermission]