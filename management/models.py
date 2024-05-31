from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

PH_RANGE = (0, 14)
TEMP_RANGE = (0, 100)
TDS_RANGE = (0, 2000)

def validate_range(
        value: float | int, 
        value_range: tuple[float | int, float | int]) -> None:
    
    if len(value_range) != 2:
        raise ValueError("Invalid range: must be a tuple of exactly two values (min, max).")
    
    min_value, max_value = value_range
    if not isinstance(min_value, (int, float)) or not isinstance(max_value, (int, float)):
        raise ValueError("Invalid range values: must be integers or floats.")

    if min_value > max_value:
        raise ValueError("Invalid range: min value cannot be greater than max value.")
    
    if not (min_value <= value <= max_value):
        raise ValidationError(f'Value {value} is out of the valid range (from {min_value} to {max_value}).')


class HydroponicSystem(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hydroponic_systems')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Measurement(models.Model):
    system = models.ForeignKey(HydroponicSystem, on_delete=models.CASCADE, related_name='measurements')
    ph = models.FloatField(
        validators=[lambda value: validate_range(value, PH_RANGE)], 
        null=True, 
        blank=True)
    temperature = models.FloatField(
        validators=[lambda value: validate_range(value, TEMP_RANGE)], 
        null=True, 
        blank=True)
    tds = models.FloatField(
        validators=[lambda value: validate_range(value, TDS_RANGE)], 
        null=True, 
        blank=True)  # Total Dissolved Solids
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Measurement for {self.system.name} at {self.timestamp}"
