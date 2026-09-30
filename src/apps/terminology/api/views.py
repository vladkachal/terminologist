from __future__ import annotations

from typing import TYPE_CHECKING

from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import RefBook, RefBookElement, RefBookVersion
from .schema import (
    refbook_check_element_schema,
    refbook_element_list_schema,
    refbook_list_schema,
)
from .serializers import (
    RefBookCheckElementQuerySerializer,
    RefBookElementListQuerySerializer,
    RefBookElementListSerializer,
    RefBookListQuerySerializer,
    RefBookListSerializer,
)

if TYPE_CHECKING:
    from rest_framework.request import Request


class RefBookListAPIView(APIView):
    @refbook_list_schema
    def get(self, request: Request) -> Response:
        query_serializer = RefBookListQuerySerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)

        as_of = query_serializer.validated_data.get("date")
        if as_of is not None:
            refbooks = RefBook.objects.current(as_of)
        else:
            refbooks = RefBook.objects.all()
        serializer = RefBookListSerializer(refbooks, many=True)
        return Response({"refbooks": serializer.data}, status=status.HTTP_200_OK)


class RefBookVersionMixin(APIView):
    @staticmethod
    def get_refbook(pk: int) -> RefBook:
        refbook = RefBook.objects.filter(pk=pk).first()
        if refbook is None:
            raise NotFound(detail="Справочник не найден.", code="refbook_not_found")
        return refbook

    @staticmethod
    def get_version(refbook: RefBook, version_number: str) -> RefBookVersion:
        version = (
            RefBookVersion.objects.filter(refbook=refbook, version=version_number)
            .with_elements()
            .first()
        )
        if version is None:
            raise NotFound(
                detail="Версия справочника не найдена.",
                code="refbook_version_not_found",
            )
        return version

    @staticmethod
    def get_latest_version(
        refbook: RefBook,
        *,
        with_elements: bool = False,
    ) -> RefBookVersion:
        version = (
            RefBookVersion.objects
            .filter(refbook=refbook)
            .latest_current(with_elements=with_elements)
        )
        if version is None:
            raise NotFound(
                detail="У справочника отсутствует актуальная версия.",  # noqa: RUF001
                code="latest_version_not_found",
            )
        return version


class RefBookElementListAPIView(RefBookVersionMixin, APIView):
    @refbook_element_list_schema
    def get(self, request: Request, pk: int) -> Response:
        query_serializer = RefBookElementListQuerySerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)

        refbook = self.get_refbook(pk)
        version_number = query_serializer.validated_data.get("version")
        if version_number is not None:
            version = self.get_version(refbook, version_number)
        else:
            version = self.get_latest_version(refbook, with_elements=True)

        serializer = RefBookElementListSerializer(version.elements.all(), many=True)
        return Response({"elements": serializer.data}, status=status.HTTP_200_OK)


class RefBookCheckElementAPIView(RefBookVersionMixin, APIView):
    @refbook_check_element_schema
    def get(self, request: Request, pk: int) -> Response:
        serializer = RefBookCheckElementQuerySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        refbook = self.get_refbook(pk)
        version_number = validated_data.get("version")
        if version_number is not None:
            version = self.get_version(refbook, version_number)
        else:
            version = self.get_latest_version(refbook)

        element = RefBookElement.objects.filter(
            version=version,
            code=validated_data["code"],
            value=validated_data["value"],
        )
        if not element.exists():
            raise NotFound(
                detail="Элемент справочника не найден.",
                code="refbook_element_not_found",
            )
        return Response(status=status.HTTP_200_OK)
