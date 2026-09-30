from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TerminologyConfig(AppConfig):
    name = "apps.terminology"
    verbose_name = _("Терминология")
