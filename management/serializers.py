from rest_framework import serializers
from .models import HydroponicSystem, Measurement

class HydroponicSystemSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = HydroponicSystem
        fields = ['id', 'owner', 'name', 'description', 'created_at', 'updated_at']

class MeasurementSerializer(serializers.ModelSerializer):
    system = serializers.PrimaryKeyRelatedField(queryset=HydroponicSystem.objects.all())

    class Meta:
        model = Measurement
        fields = ['id', 'system', 'ph', 'temperature', 'tds', 'timestamp']
