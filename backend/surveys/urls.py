from django.urls import path
from .views import export_js
from drf_spectacular.utils import extend_schema


app_name = "surveys"

urlpatterns = [
    path("export/", export_js, name="export_js"),
]
