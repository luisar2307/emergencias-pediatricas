# views/staff.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import PersonalMedico
from .serializers import PersonalMedicoSerializer


class PersonalMedicoViewSet(viewsets.ModelViewSet):
    queryset = PersonalMedico.objects.all().select_related("user")
    serializer_class = PersonalMedicoSerializer
    permission_classes = [IsAuthenticated]