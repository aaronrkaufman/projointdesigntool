from django.urls import path

from .views import (create_qualtrics, export_csv, export_js, export_json,
                    import_json, preview_survey)

app_name = "surveys"

urlpatterns = [
    path("export_js/", export_js, name="export_js"),
    path("export_json/", export_json, name="export_json"),
    path("import_json/", import_json, name="import_json"),
    path("preview_survey/", preview_survey, name="preview_survey"),
    path("export_csv/", export_csv, name="export_csv"),
    path("create_qualtrics/", create_qualtrics, name="create_qualtrics"),
]
