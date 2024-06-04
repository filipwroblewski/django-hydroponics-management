from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

PH_RANGE = (0, 14)
TEMP_RANGE = (0, 100)
TDS_RANGE = (0, 2000)


def validate_ph_range(value):
    validate_range(value, PH_RANGE)


def validate_temp_range(value):
    validate_range(value, TEMP_RANGE)


def validate_tds_range(value):
    validate_range(value, TDS_RANGE)


def validate_range(value, value_range):
    min_value, max_value = value_range
    if not isinstance(value, (int, float)):
        raise ValueError(
            "Invalid value: must be an integer or float.")
    if not (min_value <= value <= max_value):
        raise ValidationError(
            (f'Value {value} is out of the valid'
             f'range (from {min_value} to {max_value}).'))


class HydroponicSystem(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='hydroponic_systems')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Measurement(models.Model):
    system = models.ForeignKey(
        HydroponicSystem,
        on_delete=models.CASCADE,
        related_name='measurements')
    ph = models.FloatField(
        validators=[validate_ph_range],
        null=True, blank=True)
    temperature = models.FloatField(
        validators=[validate_temp_range],
        null=True, blank=True)
    tds = models.FloatField(
        validators=[validate_tds_range],
        null=True, blank=True)  # Total Dissolved Solids
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        formatted_timestamp = self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        return f"Measurement for {self.system.name} at {formatted_timestamp}"
