from datetime import date
from typing import TYPE_CHECKING

from rest_framework import status
from rest_framework.test import APITestCase

from django.urls import reverse

from ..models import RefBook, RefBookElement, RefBookVersion

if TYPE_CHECKING:
    from rest_framework.response import Response


class RefBookAPITestCase(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.refbook = RefBook.objects.create(
            code="TEST",
            name="Тестовый справочник",
            description="Описание",
        )

        cls.old_version = RefBookVersion.objects.create(
            refbook=cls.refbook,
            version="1.0",
            start_date=date(2025, 1, 1),
        )
        cls.current_version = RefBookVersion.objects.create(
            refbook=cls.refbook,
            version="2.0",
            start_date=date(2026, 1, 1),
        )
        cls.future_version = RefBookVersion.objects.create(
            refbook=cls.refbook,
            version="3.0",
            start_date=date(2099, 1, 1),
        )

        RefBookElement.objects.create(
            version=cls.old_version,
            code="A",
            value="Старое значение",
        )
        RefBookElement.objects.create(
            version=cls.current_version,
            code="A",
            value="Текущее значение",
        )
        RefBookElement.objects.create(
            version=cls.current_version,
            code="B",
            value="Второе значение",
        )
        RefBookElement.objects.create(
            version=cls.future_version,
            code="A",
            value="Будущее значение",
        )

    def assert_error_code(self, response: Response, code: str) -> None:
        self.assertEqual(response.json()["errors"][0]["code"], code)

    def test_refbook_list_returns_all_refbooks_without_date(self) -> None:
        url = reverse("api:terminology:refbook-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "refbooks": [
                    {
                        "id": self.refbook.pk,
                        "code": "TEST",
                        "name": "Тестовый справочник",
                    }
                ]
            },
        )

    def test_refbook_list_with_date_returns_refbooks_with_active_version(self) -> None:
        url = reverse("api:terminology:refbook-list")
        response = self.client.get(url, {"date": "2025-06-01"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()["refbooks"]), 1)
        self.assertEqual(
            response.json()["refbooks"][0]["id"],
            self.refbook.pk,
        )

    def test_refbook_list_with_date_excludes_refbook_without_started_version(
        self,
    ) -> None:
        future_refbook = RefBook.objects.create(
            code="FUTURE",
            name="Будущий справочник",
        )
        RefBookVersion.objects.create(
            refbook=future_refbook,
            version="1.0",
            start_date=date(2099, 1, 1),
        )
        url = reverse("api:terminology:refbook-list")
        response = self.client.get(url, {"date": "2026-01-01"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        refbook_ids = {item["id"] for item in response.json()["refbooks"]}
        self.assertIn(self.refbook.pk, refbook_ids)
        self.assertNotIn(future_refbook.pk, refbook_ids)

    def test_refbook_list_rejects_invalid_date(self) -> None:
        url = reverse("api:terminology:refbook-list")
        response = self.client.get(url, {"date": "01.01.2026"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_elements_without_version_use_latest_current_version(self) -> None:
        url = reverse(
            "api:terminology:refbook-elements",
            kwargs={"pk": self.refbook.pk},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "elements": [
                    {"code": "A", "value": "Текущее значение"},
                    {"code": "B", "value": "Второе значение"},
                ]
            },
        )

    def test_elements_with_version_return_requested_version(self) -> None:
        url = reverse(
            "api:terminology:refbook-elements",
            kwargs={"pk": self.refbook.pk},
        )
        response = self.client.get(url, {"version": "1.0"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "elements": [
                    {"code": "A", "value": "Старое значение"},
                ]
            },
        )

    def test_elements_do_not_use_future_version_as_current(self) -> None:
        url = reverse(
            "api:terminology:refbook-elements",
            kwargs={"pk": self.refbook.pk},
        )
        response = self.client.get(url)
        values = {element["value"] for element in response.json()["elements"]}
        self.assertNotIn("Будущее значение", values)

    def test_elements_return_404_for_unknown_refbook(self) -> None:
        url = reverse(
            "api:terminology:refbook-elements",
            kwargs={"pk": 999999},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assert_error_code(response, "refbook_not_found")

    def test_elements_return_404_for_unknown_version(self) -> None:
        url = reverse(
            "api:terminology:refbook-elements",
            kwargs={"pk": self.refbook.pk},
        )
        response = self.client.get(url, {"version": "999.0"})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assert_error_code(response, "refbook_version_not_found")

    def test_check_element_returns_200_for_exact_match(self) -> None:
        url = reverse(
            "api:terminology:refbook-check-element",
            kwargs={"pk": self.refbook.pk},
        )
        response = self.client.get(
            url,
            {
                "code": "A",
                "value": "Текущее значение",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, b"")

    def test_check_element_uses_requested_version(self) -> None:
        url = reverse(
            "api:terminology:refbook-check-element",
            kwargs={"pk": self.refbook.pk},
        )
        response = self.client.get(
            url,
            {
                "code": "A",
                "value": "Старое значение",
                "version": "1.0",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_check_element_returns_404_for_wrong_value(self) -> None:
        url = reverse(
            "api:terminology:refbook-check-element",
            kwargs={"pk": self.refbook.pk},
        )
        response = self.client.get(
            url,
            {
                "code": "A",
                "value": "Неверное значение",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assert_error_code(response, "refbook_element_not_found")

    def test_check_element_requires_code(self) -> None:
        url = reverse(
            "api:terminology:refbook-check-element",
            kwargs={"pk": self.refbook.pk},
        )
        response = self.client.get(
            url,
            {"value": "Текущее значение"},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_check_element_requires_value(self) -> None:
        url = reverse(
            "api:terminology:refbook-check-element",
            kwargs={"pk": self.refbook.pk},
        )
        response = self.client.get(
            url,
            {"code": "A"},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_check_element_rejects_blank_code(self) -> None:
        url = reverse(
            "api:terminology:refbook-check-element",
            kwargs={"pk": self.refbook.pk},
        )
        response = self.client.get(
            url,
            {
                "code": "",
                "value": "Текущее значение",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
