from __future__ import annotations

from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
    inline_serializer,
)
from rest_framework import serializers

# ---------------------------------------------------------------------------
# GET /refbooks/
# ---------------------------------------------------------------------------

refbook_list_schema = extend_schema(
    operation_id="refbooks_list",
    summary="Получение списка справочников",
    description=(
        "Возвращает список справочников. Если указан параметр `date`, возвращаются "
        "только те справочники, у которых существует версия с датой начала "  # noqa RUF001
        "действия, не превышающей указанную дату."
    ),
    parameters=[
        OpenApiParameter(
            name="date",
            type=str,
            location=OpenApiParameter.QUERY,
            required=False,
            description=(
                "Дата в формате ГГГГ-ММ-ДД. Возвращаются справочники, имеющие версию "  # noqa RUF001
                "с датой начала действия не позже указанной даты."  # noqa RUF001
            ),
            examples=[
                OpenApiExample("2020-01-01", value="2020-01-01"),
                OpenApiExample("2024-01-01", value="2024-01-01"),
                OpenApiExample("2026-10-01", value="2026-10-01"),
            ],
        ),
    ],
    responses={
        200: OpenApiResponse(
            response=inline_serializer(
                name="RefbookListResponse",
                fields={
                    "refbooks": serializers.ListField(
                        child=inline_serializer(
                            name="RefbookListItem",
                            fields={
                                "id": serializers.CharField(
                                    help_text="Идентификатор справочника.",
                                ),
                                "code": serializers.CharField(
                                    help_text="Код справочника.",
                                ),
                                "name": serializers.CharField(
                                    help_text="Наименование справочника.",
                                ),
                            },
                        ),
                    ),
                },
            ),
            description="Список справочников.",
            examples=[
                OpenApiExample(
                    "Успешный ответ",
                    value={
                        "refbooks": [
                            {
                                "id": "MS1",
                                "code": "MS1",
                                "name": "Специальности медицинских работников",
                            },
                            {
                                "id": "ICD-10",
                                "code": "ICD-10",
                                "name": "МКБ-10",
                            },
                        ],
                    },
                ),
            ],
        ),
    },
    tags=["Справочники"],
)


# ---------------------------------------------------------------------------
# GET /refbooks/{id}/elements/
# ---------------------------------------------------------------------------

refbook_element_list_schema = extend_schema(
    operation_id="refbook_elements",
    summary="Получение элементов справочника",
    description=(
        "Возвращает элементы указанного справочника. Если параметр `version` указан, "
        "возвращаются элементы соответствующей версии. Если параметр не указан, "
        "используется текущая версия справочника: версия с максимальной датой начала "  # noqa RUF001
        "действия, которая не позже текущей даты."
    ),
    parameters=[
        OpenApiParameter(
            name="id",
            type=int,
            location=OpenApiParameter.PATH,
            required=True,
            description="Идентификатор справочника.",
            examples=[
                OpenApiExample("1", value=1),
            ],
        ),
        OpenApiParameter(
            name="version",
            type=str,
            location=OpenApiParameter.QUERY,
            required=False,
            description=(
                "Версия справочника. Если не указана, используется текущая версия."
            ),
            examples=[
                OpenApiExample("1.0", value="1.0"),
            ],
        ),
    ],
    responses={
        200: OpenApiResponse(
            response=inline_serializer(
                name="RefbookElementsResponse",
                fields={
                    "elements": serializers.ListField(
                        child=inline_serializer(
                            name="RefbookElementItem",
                            fields={
                                "code": serializers.CharField(
                                    help_text="Код элемента.",
                                ),
                                "value": serializers.CharField(
                                    help_text="Значение элемента.",
                                ),
                            },
                        ),
                    ),
                },
            ),
            description="Элементы выбранной версии справочника.",
            examples=[
                OpenApiExample(
                    "Успешный ответ",
                    value={
                        "elements": [
                            {
                                "code": "J00",
                                "value": "Острый назофарингит (насморк)",
                            },
                            {
                                "code": "J01",
                                "value": "Острый синусит",
                            },
                        ],
                    },
                ),
            ],
        ),
    },
    tags=["Справочники"],
)


# ---------------------------------------------------------------------------
# GET /refbooks/{id}/check_element/
# ---------------------------------------------------------------------------

refbook_check_element_schema = extend_schema(
    operation_id="refbook_check_element",
    summary="Проверка элемента справочника",
    description=(
        "Проверяет наличие элемента с указанным кодом и значением в выбранной версии "  # noqa RUF001
        "справочника. Если версия не указана, используется текущая версия справочника: "
        "версия с максимальной датой начала действия, которая не позже текущей даты."  # noqa RUF001
    ),
    parameters=[
        OpenApiParameter(
            name="id",
            type=int,
            location=OpenApiParameter.PATH,
            required=True,
            description="Идентификатор справочника.",
            examples=[
                OpenApiExample("1", value=1),
            ],
        ),
        OpenApiParameter(
            name="code",
            type=str,
            location=OpenApiParameter.QUERY,
            required=True,
            description="Код элемента справочника.",
            examples=[
                OpenApiExample("1", value="1"),
            ],
        ),
        OpenApiParameter(
            name="value",
            type=str,
            location=OpenApiParameter.QUERY,
            required=True,
            description="Значение элемента справочника.",
            examples=[
                OpenApiExample(
                    "Врач-терапевт",
                    value="Врач-терапевт",
                ),
            ],
        ),
        OpenApiParameter(
            name="version",
            type=str,
            location=OpenApiParameter.QUERY,
            required=False,
            description=(
                "Версия справочника. Если не указана, используется текущая версия."
            ),
            examples=[
                OpenApiExample("1.0", value="1.0"),
            ],
        ),
    ],
    responses={
        200: OpenApiResponse(
            response=inline_serializer(
                name="CheckElementResponse",
                fields={},
            ),
            description="Результат проверки элемента.",
            examples=[
                OpenApiExample(
                    "Элемент существует",
                ),
                OpenApiExample(
                    "Элемент отсутствует",
                ),
            ],
        ),
    },
    tags=["Справочники"],
)
