from django.urls import path

from .views import (
    RefBookCheckElementAPIView,
    RefBookElementListAPIView,
    RefBookListAPIView,
)

app_name = "terminology"

urlpatterns = [
    path(
        "",
        RefBookListAPIView.as_view(),
        name="refbook-list",
    ),
    path(
        "<int:pk>/elements/",
        RefBookElementListAPIView.as_view(),
        name="refbook-elements",
    ),
    path(
        "<int:pk>/check_element/",
        RefBookCheckElementAPIView.as_view(),
        name="refbook-check-element",
    ),
]
