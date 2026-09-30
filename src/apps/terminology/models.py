from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from .exceptions import CurrentVersionNotPrefetchedError
from .managers import RefBookElementManager, RefBookManager, RefBookVersionManager


class RefBook(models.Model):
    code = models.CharField(max_length=100, unique=True, verbose_name=_("Код"))
    name = models.CharField(max_length=300, verbose_name=_("Наименование"))
    description = models.TextField(blank=True, default="", verbose_name=_("Описание"))

    objects = RefBookManager()

    class Meta:
        verbose_name = _("Справочник")
        verbose_name_plural = _("Справочники")
        ordering = ("-id",)
        constraints = [
            models.CheckConstraint(
                condition=~Q(code=""),
                name="refbook_code_not_empty",
            ),
            models.CheckConstraint(
                condition=~Q(name=""),
                name="refbook_name_not_empty",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.code} — {self.name}"

    @property
    def current_version(self) -> RefBookVersion | None:
        if not hasattr(self, "_current_versions"):
            raise CurrentVersionNotPrefetchedError(self.pk)
        versions = self._current_versions
        return versions[0] if versions else None


class RefBookVersion(models.Model):
    refbook = models.ForeignKey(
        RefBook,
        on_delete=models.PROTECT,
        related_name="versions",
        verbose_name=_("Справочник"),
    )
    version = models.CharField(max_length=50, verbose_name=_("Версия"))
    start_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Дата начала действия"),
    )

    objects = RefBookVersionManager()

    class Meta:
        verbose_name = _("Версия справочника")
        verbose_name_plural = _("Версии справочников")
        ordering = ("refbook__code", "-start_date", "-id")
        constraints = [
            models.UniqueConstraint(
                fields=("refbook", "version"),
                name="unique_refbook_version",
            ),
            models.UniqueConstraint(
                fields=("refbook", "start_date"),
                name="unique_refbook_start_date",
            ),
            models.CheckConstraint(
                condition=~Q(version=""),
                name="refbook_version_not_empty",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.refbook.code} — {self.version}"


class RefBookElement(models.Model):
    version = models.ForeignKey(
        RefBookVersion,
        on_delete=models.PROTECT,
        related_name="elements",
        verbose_name=_("Версия справочника"),
    )
    code = models.CharField(max_length=100, verbose_name=_("Код элемента"))
    value = models.CharField(max_length=300, verbose_name=_("Значение элемента"))

    objects = RefBookElementManager()

    class Meta:
        verbose_name = _("Элемент справочника")
        verbose_name_plural = _("Элементы справочника")
        ordering = ("code", "id")
        constraints = [
            models.UniqueConstraint(
                fields=("version", "code"),
                name="unique_version_element_code",
            ),
            models.CheckConstraint(
                condition=~Q(code=""),
                name="refelement_code_not_empty",
            ),
            models.CheckConstraint(
                condition=~Q(value=""),
                name="refelement_value_not_empty",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.code} — {self.value}"
