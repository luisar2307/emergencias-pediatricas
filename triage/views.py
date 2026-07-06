from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Triaje
from .serializers import TriajeSerializer, TriajeDetalleSerializer


class TriajeViewSet(viewsets.ModelViewSet):
    queryset = Triaje.objects.all().select_related("paciente", "personal__user")
    permission_classes = [IsAuthenticated]

    # Alterna dinámicamente los serializers según la acción (Lectura vs Escritura)
    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return TriajeDetalleSerializer
        return TriajeSerializer
