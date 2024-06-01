from rest_framework import viewsets, permissions
from .models import HydroponicSystem, Measurement
from .serializers import HydroponicSystemSerializer, MeasurementSerializer
from django.core.exceptions import PermissionDenied

def check_owner_permission(request_user, instance_owner):
    if request_user != instance_owner:
        raise PermissionDenied("You do not have permission for this action.")
    
class HydroponicSystemViewSet(viewsets.ModelViewSet):
    queryset = HydroponicSystem.objects.all()
    serializer_class = HydroponicSystemSerializer
    permission_classes = [permissions.IsAuthenticated]

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
