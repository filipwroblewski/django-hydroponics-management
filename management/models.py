from django.db import models
from django.contrib.auth.models import User

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
    ph = models.FloatField()
    temperature = models.FloatField()
    tds = models.FloatField()  # Total Dissolved Solids
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Measurement for {self.system.name} at {self.timestamp}"
