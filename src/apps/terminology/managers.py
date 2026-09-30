from __future__ import annotations

from typing import TYPE_CHECKING, Self

from django.db import models
from django.db.models import Prefetch
from django.utils import timezone

if TYPE_CHECKING:
    from .models import RefBook, RefBookElement, RefBookVersion  # noqa F401
    from datetime import date


class RefBookQuerySet(models.QuerySet["RefBook"]):
    def with_versions(self) -> Self:
        return self.prefetch_related("versions")

    def with_current_version(self, as_of: date | None = None) -> Self:
        from apps.terminology.models import RefBookVersion

        as_of = as_of or timezone.localdate()
        current_versions = RefBookVersion.objects.current(as_of=as_of).order_by(
            "-start_date", "-pk"
        )
        return self.prefetch_related(
            Prefetch(
                "versions",
                queryset=current_versions,
                to_attr="_current_versions",
            )
        )

    def current(self, as_of: date) -> Self:
        return self.filter(
            versions__start_date__isnull=False,
            versions__start_date__lte=as_of,
        ).distinct()


class RefBookManager(models.Manager.from_queryset(RefBookQuerySet)):
    pass


class RefBookVersionQuerySet(models.QuerySet["RefBookVersion"]):
    def current(self, as_of: date | None = None) -> Self:
        as_of = as_of or timezone.localdate()
        return self.filter(start_date__isnull=False, start_date__lte=as_of)

    def latest_current(self, as_of: date | None = None) -> RefBookVersion | None:
        return self.current(as_of).order_by("-start_date", "-pk").first()

    def with_refbook(self) -> Self:
        return self.select_related("refbook")

    def with_elements(self) -> Self:
        return self.prefetch_related("elements")


class RefBookVersionManager(models.Manager.from_queryset(RefBookVersionQuerySet)):
    pass


class RefBookElementQuerySet(models.QuerySet["RefBookElement"]):
    def with_version_and_refbook(self) -> Self:
        return self.select_related("version__refbook")


class RefBookElementManager(models.Manager.from_queryset(RefBookElementQuerySet)):
    pass
