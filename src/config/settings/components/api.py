from pathlib import Path

from ..base import BASE_DIR

# ------------------------------------------------------------------------------
# DJANGO-REST-FRAMEWORK (DRF)
# ------------------------------------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_PAGINATION_CLASS": ("config.api.pagination.StandardPageNumberPagination"),
    "DEFAULT_SCHEMA_CLASS": "drf_standardized_errors.openapi.AutoSchema",
    "EXCEPTION_HANDLER": "drf_standardized_errors.handler.exception_handler",
}

# ------------------------------------------------------------------------------
# DRF-SPECTACULAR
# ------------------------------------------------------------------------------
with Path.open(BASE_DIR / "config" / "api" / "docs" / "description.md", "r") as f:
    _api_description = f.read()

SPECTACULAR_SETTINGS = {
    "TITLE": "Terminology API",
    "VERSION": "0.1.0",
    "OAS_VERSION": "3.1.0",
    "DESCRIPTION": _api_description,
    "SERVE_PERMISSIONS": ["rest_framework.permissions.AllowAny"],
    "SERVE_INCLUDE_SCHEMA": False,
    "SWAGGER_UI_SETTINGS": {
        "persistAuthorization": True,
        "filter": True,
        "deepLinking": True,
        "tagsSorter": "alpha",
        "defaultModelsExpandDepth": -1,
        "tryItOutEnabled": True,
    },
    "POSTPROCESSING_HOOKS": [
        "drf_standardized_errors.openapi_hooks.postprocess_schema_enums",
    ],
    "ENUM_NAME_OVERRIDES": {},
}
for enum in [
    "ValidationErrorEnum",
    "ClientErrorEnum",
    "ServerErrorEnum",
    "ErrorCode401Enum",
    "ErrorCode403Enum",
    "ErrorCode404Enum",
    "ErrorCode405Enum",
    "ErrorCode406Enum",
    "ErrorCode415Enum",
    "ErrorCode429Enum",
    "ErrorCode500Enum",
]:
    SPECTACULAR_SETTINGS["ENUM_NAME_OVERRIDES"][enum] = (
        f"drf_standardized_errors.openapi_serializers.{enum}.choices",
    )

# ------------------------------------------------------------------------------
# DRF-STANDARDIZED-ERRORS
# ------------------------------------------------------------------------------
DRF_STANDARDIZED_ERRORS = {
    "ENABLE_IN_DEBUG_FOR_UNHANDLED_EXCEPTIONS": True,
    "EXCEPTION_FORMATTER_CLASS": (
        "drf_standardized_errors.formatter.ExceptionFormatter"
    ),
    "ALLOWED_ERROR_STATUS_CODES": ["400", "403", "404", "429"],
}
