from django.urls import path
from .views import export_js

urlpatterns = [
    path("export/", export_js, name="export_js"),
]
