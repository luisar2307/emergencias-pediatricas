from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Paciente, Tutor

from .serializers import (
    PacienteSerializer,
    PacienteCreateUpdateSerializer,
    PacienteListSerializer,
    TutorSerializer
)


class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Paciente.objects.prefetch_related('tutores', 'antecedente_medico').all()

    def get_serializer_class(self):
        if self.action == 'list':
            return PacienteListSerializer
        if self.action in ['create', 'update', 'partial_update']:
            return PacienteCreateUpdateSerializer
        return PacienteSerializer

    @action(detail=True, methods=['post'])
    def agregar_tutor(self, request, pk=None):
        paciente = self.get_object()
        serializer = TutorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(paciente=paciente)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def tutores(self, request, pk=None):
        paciente = self.get_object()
        tutores = paciente.tutores.all()
        serializer = TutorSerializer(tutores, many=True)
        return Response(serializer.data)


class TutorViewSet(viewsets.ModelViewSet):
    queryset = Tutor.objects.select_related('paciente').all()
    serializer_class = TutorSerializer