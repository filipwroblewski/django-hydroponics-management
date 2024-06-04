from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    HydroponicSystemViewSet,
    MeasurementViewSet)

router = DefaultRouter()
router.register(
    r'hydroponic-systems',
    HydroponicSystemViewSet,
    basename='hydroponic-system')
router.register(
    r'measurements',
    MeasurementViewSet,
    basename='measurement')

urlpatterns = [
    path('', include(router.urls)),
]
