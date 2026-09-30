from __future__ import annotations

from rest_framework import serializers

from ..models import RefBook, RefBookElement


class RefBookListSerializer(serializers.ModelSerializer):
    class Meta:
        model = RefBook
        fields = ("id", "code", "name")


class RefBookListQuerySerializer(serializers.Serializer):
    date = serializers.DateField(
        required=False,
        input_formats=("%Y-%m-%d",),
        error_messages={
            "invalid": "Параметр 'date' должен быть в формате ГГГГ-ММ-ДД.",  # noqa RUF001
        },
    )


class RefBookElementListSerializer(serializers.ModelSerializer):
    class Meta:
        model = RefBookElement
        fields = ("code", "value")


class RefBookElementListQuerySerializer(serializers.Serializer):
    version = serializers.CharField(
        max_length=50,
        required=False,
        allow_blank=False,
        trim_whitespace=True,
    )


class RefBookCheckElementQuerySerializer(serializers.Serializer):
    code = serializers.CharField(
        max_length=100,
        allow_blank=False,
        trim_whitespace=True,
    )
    value = serializers.CharField(
        max_length=300,
        allow_blank=False,
        trim_whitespace=True,
    )
    version = serializers.CharField(
        max_length=50,
        required=False,
        allow_blank=False,
        trim_whitespace=True,
    )
