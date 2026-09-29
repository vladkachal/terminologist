from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerSplitView,
)

from django.urls import path

app_name = "docs"

urlpatterns = [
    path(
        "schema/",
        SpectacularAPIView.as_view(),
        name="schema",
    ),
    path(
        "",
        SpectacularSwaggerSplitView.as_view(url_name="api:docs:schema"),
        name="swagger_ui",
    ),
    path(
        "redoc/",
        SpectacularRedocView.as_view(url_name="api:docs:schema"),
        name="redoc",
    ),
]
