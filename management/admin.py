from django.contrib import admin
from .models import HydroponicSystem, Measurement

        
class HydroponicSystemAdmin(admin.ModelAdmin):
    list_display = ['id', 'owner', 'name', 'description', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']
    list_filter = ['owner', ('created_at', admin.DateFieldListFilter), ('updated_at', admin.DateFieldListFilter)]

class MeasurementAdmin(admin.ModelAdmin):
    list_display = ['id', 'system', 'ph', 'temperature', 'tds', 'timestamp']
    readonly_fields = ['timestamp']
    list_filter = ['system', ('timestamp', admin.DateFieldListFilter)]

admin.site.register(HydroponicSystem, HydroponicSystemAdmin)
admin.site.register(Measurement, MeasurementAdmin)