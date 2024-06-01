from rest_framework import viewsets, permissions
from .models import HydroponicSystem, Measurement
from .serializers import HydroponicSystemSerializer, MeasurementSerializer
from django.core.exceptions import ValidationError

class HydroponicSystemViewSet(viewsets.ModelViewSet):
    queryset = HydroponicSystem.objects.all()
    serializer_class = HydroponicSystemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return HydroponicSystem.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class MeasurementViewSet(viewsets.ModelViewSet):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Measurement.objects.filter(system__owner=self.request.user)

    def perform_create(self, serializer):
        system = HydroponicSystem.objects.get(id=self.request.data['system'])
        if system.owner != self.request.user:
            raise ValidationError('You do not have permission to add measurements to this system.')
        serializer.save()
