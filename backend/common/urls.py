from django.urls import path
from .views import (
    tooltip
)

urlpatterns = [
    path('tooltips/<str:identifier>/', tooltip, name='tooltip-detail'),
]
