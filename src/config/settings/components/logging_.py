import logging

from pathlib import Path

from decouple import config

from ..base import ADMINS, BASE_DIR, CurrentEnv

LOG_DIR = BASE_DIR / "logs"
Path(LOG_DIR).mkdir(parents=True, exist_ok=True)

LOG_LEVEL_DEFAULT = config("LOG_LEVEL_DEFAULT", default=logging.ERROR)
LOG_LEVEL_DJANGO = config("LOG_LEVEL_DJANGO", default=LOG_LEVEL_DEFAULT)
LOG_LEVEL_APPS = config("LOG_LEVEL_APPS", default=LOG_LEVEL_DEFAULT)

SEND_LOGS_TO_ADMINS = config("SEND_LOGS_TO_ADMINS", default=True, cast=bool)
WRITE_LOGS_TO_FILE = config("WRITE_LOGS_TO_FILE", default=True, cast=bool)

LOG_DATE_FORMAT = "%H:%M:%S" if CurrentEnv.is_dev else "%Y-%m-%d %H:%M:%S"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "mail_admins_enabled": {
            "()": "django.utils.log.CallbackFilter",
            "callback": lambda _: SEND_LOGS_TO_ADMINS and bool(ADMINS),
        },
        "write_logs_to_file_enabled": {
            "()": "django.utils.log.CallbackFilter",
            "callback": lambda _: WRITE_LOGS_TO_FILE,
        },
    },
    "formatters": {
        "default": {
            "format": "{asctime} {levelname:<8} {message}   <- {name}:{lineno}",
            "style": "{",
            "datefmt": LOG_DATE_FORMAT,
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filters": ["write_logs_to_file_enabled"],
            "formatter": "default",
            "filename": LOG_DIR / "django.log",
            "maxBytes": 10 * 1024 * 1024,
            "backupCount": 5,
        },
        "mail_admins": {
            "class": "django.utils.log.AdminEmailHandler",
            "filters": ["mail_admins_enabled"],
            "formatter": "default",
            "level": LOG_LEVEL_DEFAULT,
        },
    },
    "root": {
        "handlers": ["console", "file", "mail_admins"],
        "level": LOG_LEVEL_DEFAULT,
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file", "mail_admins"],
            "level": LOG_LEVEL_DJANGO,
            "propagate": False,
        },
        "apps": {
            "handlers": ["console", "file", "mail_admins"],
            "level": LOG_LEVEL_APPS,
            "propagate": False,
        },
    },
}
