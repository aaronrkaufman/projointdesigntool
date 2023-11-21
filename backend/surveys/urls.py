from django.urls import path
from .views import export_js, list_user_surveys, save_user_survey, preview_survey, create_qualtrics


app_name = "surveys"

urlpatterns = [
    path("export/", export_js, name="export"),
    path("list/", list_user_surveys, name="list"),
    path("save/", save_user_survey, name="save"),
    path("qualtrics/", create_qualtrics, name="qualtrics")
    path("preview/", preview_survey, name="preview"),
]
