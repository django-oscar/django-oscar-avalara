from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AvalaraConfig(AppConfig):
    label = 'avalara'
    name = 'avalara'
    verbose_name = _('Avalara')
