from django.urls import path
from .views import (
    markdown_content_view
)

app_name = "dmd_app"

urlpatterns = [
    path("markdown_content_view/", markdown_content_view, name="markdown_content_view"),
]
