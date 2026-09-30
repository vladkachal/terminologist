from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib import admin

from .models import RefBook, RefBookElement, RefBookVersion

if TYPE_CHECKING:
    from datetime import date

    from django.db.models import QuerySet
    from django.http import HttpRequest


class RefBookVersionInline(admin.TabularInline):
    model = RefBookVersion
    extra = 0
    min_num = 0
    can_delete = True
    show_change_link = True
    fields = ("version", "start_date")
    ordering = ("-start_date", "-id")

    def get_queryset(self, request: HttpRequest) -> QuerySet[RefBookVersion]:
        return super().get_queryset(request).with_refbook()


@admin.register(RefBook)
class RefBookAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "code",
        "name",
        "current_version_display",
        "current_version_date_display",
    )
    search_fields = ("code", "name", "description")
    inlines = (RefBookVersionInline,)
    save_on_top = True

    def get_queryset(self, request: HttpRequest) -> QuerySet[RefBook]:
        return super().get_queryset(request).with_current_version()

    @admin.display(description="Текущая версия", ordering="current_version_number")
    def current_version_display(self, obj: RefBook) -> str:
        return obj.current_version.version or "-"

    @admin.display(
        description="Дата начала действия версии", ordering="current_version_date"
    )
    def current_version_date_display(self, obj: RefBook) -> date | str:
        return obj.current_version.start_date or "-"


class RefBookElementInline(admin.TabularInline):
    model = RefBookElement
    extra = 0
    min_num = 0
    can_delete = True
    fields = ("code", "value")
    ordering = ("code", "id")


@admin.register(RefBookVersion)
class RefBookVersionAdmin(admin.ModelAdmin):
    list_display = ("id", "refbook_code", "refbook_name", "version", "start_date")
    list_select_related = ("refbook",)
    search_fields = ("version", "refbook__code", "refbook__name")
    list_filter = ("start_date",)
    ordering = ("refbook__code", "-start_date", "-id")
    fields = ("refbook", "version", "start_date")
    inlines = (RefBookElementInline,)
    save_on_top = True

    @admin.display(description="Код справочника", ordering="refbook__code")
    def refbook_code(self, obj: RefBookVersion) -> str:
        return obj.refbook.code

    @admin.display(description="Наименование справочника", ordering="refbook__name")
    def refbook_name(self, obj: RefBookVersion) -> str:
        return obj.refbook.name


@admin.register(RefBookElement)
class RefBookElementAdmin(admin.ModelAdmin):
    list_display = ("id", "refbook_code", "version", "code", "value")
    list_select_related = ("version", "version__refbook")
    search_fields = (
        "code",
        "value",
        "version__version",
        "version__refbook__code",
        "version__refbook__name",
    )
    list_filter = ("version__refbook", "version")
    ordering = ("version__refbook__code", "version__version", "code", "id")
    fields = ("version", "code", "value")
    save_on_top = True

    @admin.display(description="Код справочника", ordering="version__refbook__code")
    def refbook_code(self, obj: RefBookElement) -> str:
        return obj.version.refbook.code

    @admin.display(description="Версия", ordering="version__version")
    def version(self, obj: RefBookElement) -> str:
        return obj.version.version
