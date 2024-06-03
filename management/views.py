from rest_framework import (
    viewsets,
    permissions,
    filters,
    status)
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import (
    HydroponicSystem,
    Measurement)
from .serializers import (
    HydroponicSystemSerializer,
    MeasurementSerializer)
from .filters import (
    HydroponicSystemFilter,
    MeasurementFilter)
from .utils import check_owner_permission
from django_filters.rest_framework import DjangoFilterBackend
from django.core.exceptions import ObjectDoesNotExist


class PaginationMixin:
    def paginate_queryset(self, queryset):
        queryset = queryset.order_by('id')
        return super().paginate_queryset(queryset)


class BasePermissionViewSet(PaginationMixin, viewsets.ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(
            owner=self.request.user)

    def perform_destroy(self, instance):
        check_owner_permission(
            self.request.user, instance.owner)
        instance.delete()

    def perform_update(self, serializer):
        instance = self.get_object()
        check_owner_permission(
            self.request.user, instance.owner)
        serializer.save()


class HydroponicSystemViewSet(BasePermissionViewSet):
    queryset = HydroponicSystem.objects.all()
    serializer_class = HydroponicSystemSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter]
    filterset_class = HydroponicSystemFilter
    search_fields = ['name', 'description']

    def get_queryset(self):
        return HydroponicSystem.objects.filter(
            owner=self.request.user)

    def paginate_queryset(self, queryset):
        queryset = queryset.order_by('name')
        return super().paginate_queryset(queryset)


class MeasurementViewSet(BasePermissionViewSet):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter]
    filterset_class = MeasurementFilter
    ordering_fields = ['ph', 'temperature', 'tds', 'timestamp']

    def get_queryset(self):
        return Measurement.objects.filter(
            system__owner=self.request.user)

    def perform_create(self, serializer):
        try:
            system = HydroponicSystem.objects.get(
                id=self.request.data['system'])
            check_owner_permission(
                self.request.user,
                system.owner)
            serializer.save()
        except ObjectDoesNotExist:
            return Response(
                {"error": "Hydroponic system not found."},
                status=status.HTTP_404_NOT_FOUND)

    def perform_update(self, serializer):
        instance = self.get_object()
        check_owner_permission(
            self.request.user, instance.system.owner)
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()

    @action(
            detail=False,
            methods=['get'],
            url_path='last-measurements')
    def last_measurements(self, request):
        system_name = request.query_params.get('system_name')
        num_measurements = request.query_params.get(
            'num_measurements', 10)

        try:
            num_measurements = int(num_measurements)
        except ValueError:
            return Response({
                "error": "num_measurements must be an integer."},
                status=status.HTTP_400_BAD_REQUEST)

        try:
            system = HydroponicSystem.objects.get(
                name=system_name, owner=request.user)
            measurements = Measurement.objects.filter(
                system=system).order_by(
                    '-timestamp')[:num_measurements]
            serializer = MeasurementSerializer(measurements, many=True)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response({
                "error": "System not found or you do not have permission."},
                status=status.HTTP_404_NOT_FOUND)
