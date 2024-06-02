import django_filters
from .models import HydroponicSystem

class HydroponicSystemFilter(django_filters.FilterSet):
    created_at = django_filters.DateFromToRangeFilter()
    updated_at = django_filters.DateFromToRangeFilter()

    class Meta:
        model = HydroponicSystem
        fields = ['created_at', 'updated_at']
