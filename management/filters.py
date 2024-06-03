import django_filters
from .models import HydroponicSystem, Measurement

class HydroponicSystemFilter(django_filters.FilterSet):
    created_at = django_filters.DateFromToRangeFilter()
    updated_at = django_filters.DateFromToRangeFilter()

    class Meta:
        model = HydroponicSystem
        fields = ['created_at', 'updated_at']

class MeasurementFilter(django_filters.FilterSet):
    """
    Filter class which provides (min/max) range filters for pH, temperature, and TDS values.
    """
    
    ph_min = django_filters.NumberFilter(field_name='ph', lookup_expr='gte')
    ph_max = django_filters.NumberFilter(field_name='ph', lookup_expr='lte')

    temperature_min = django_filters.NumberFilter(field_name='temperature', lookup_expr='gte')
    temperature_max = django_filters.NumberFilter(field_name='temperature', lookup_expr='lte')
    
    tds_min = django_filters.NumberFilter(field_name='tds', lookup_expr='gte')
    tds_max = django_filters.NumberFilter(field_name='tds', lookup_expr='lte')

    class Meta:
        model = Measurement
        fields = ['system', 'ph', 'temperature', 'tds', 'timestamp']