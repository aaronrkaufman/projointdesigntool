from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),
    # Swagger urls
    path("schema/", SpectacularAPIView.as_view(), name="schema"),

    # path("api/profiles/", include("profiles.urls")),
    path("api/surveys/", include("surveys.urls")),
    path("api/common/", include("common.urls")),

    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema")
    ),
]
