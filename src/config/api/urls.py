from django.urls import include, path

app_name = "api"

urlpatterns = [
    path("docs/", include("config.api.docs.urls")),
    path("refbooks/", include("apps.terminology.api.urls")),
]
