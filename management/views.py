from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
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
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = HydroponicSystemFilter
    search_fields = ['name', 'description']

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
    
    @action(detail=False, methods=['get'], url_path='last-measurements')
    def last_measurements(self, request):
        system_name = request.query_params.get('system_name')
        num_measurements = request.query_params.get('num_measurements', 10)
        
        try:
            num_measurements = int(num_measurements)
        except ValueError:
            return Response({"error": "num_measurements must be an integer."}, status=400)
        
        system = HydroponicSystem.objects.filter(name=system_name, owner=request.user).first()
        if not system:
            return Response({"error": "System not found or you do not have permission."}, status=404)
        
        measurements = Measurement.objects.filter(system=system).order_by('-timestamp')[:num_measurements]
        serializer = MeasurementSerializer(measurements, many=True)
        return Response(serializer.data)
