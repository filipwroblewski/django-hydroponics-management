from rest_framework import viewsets, permissions, filters
from .models import HydroponicSystem, Measurement
from .serializers import HydroponicSystemSerializer, MeasurementSerializer
from .filters import HydroponicSystemFilter, MeasurementFilter
from django.core.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend

def check_owner_permission(request_user, instance_owner):
    if request_user != instance_owner:
        raise PermissionDenied("You do not have permission for this action.")
    
class HydroponicSystemViewSet(viewsets.ModelViewSet):
    queryset = HydroponicSystem.objects.all()
    serializer_class = HydroponicSystemSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = HydroponicSystemFilter

    def get_queryset(self):
        return HydroponicSystem.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
    def perform_destroy(self, instance):
        check_owner_permission(self.request.user, instance.owner)
        instance.delete()
    
    def perform_update(self, serializer):
        instance = self.get_object()
        check_owner_permission(self.request.user, instance.owner)
        serializer.save()

class MeasurementViewSet(viewsets.ModelViewSet):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = MeasurementFilter
    ordering_fields = ['ph', 'temperature', 'tds', 'timestamp']

    def get_queryset(self):
        return Measurement.objects.filter(system__owner=self.request.user)

    def perform_create(self, serializer):
        system = HydroponicSystem.objects.get(id=self.request.data['system'])
        check_owner_permission(self.request.user, system.owner)
        serializer.save()

    def perform_destroy(self, instance):
        check_owner_permission(self.request.user, instance.owner)
        instance.delete()

    def perform_update(self, serializer):
        instance = self.get_object()
        check_owner_permission(self.request.user, instance.system.owner)
        serializer.save()
