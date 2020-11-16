from django.contrib.auth.models import AbstractUser, models
from django.utils.deconstruct import deconstructible
from django.utils.translation import ugettext_lazy as _
import re

from django.core import validators


class CaseInsensitiveFieldMixin:
    """
    Field mixin that uses case-insensitive lookup alternatives if they exist.
    """

    LOOKUP_CONVERSIONS = {
        'exact': 'iexact',
        'contains': 'icontains',
        'startswith': 'istartswith',
        'endswith': 'iendswith',
        'regex': 'iregex',
    }

    def get_lookup(self, lookup_name):
        converted = self.LOOKUP_CONVERSIONS.get(lookup_name, lookup_name)
        return super().get_lookup(converted)


class CICharField(CaseInsensitiveFieldMixin, models.CharField):
    pass


@deconstructible
class MyUnicodeUsernameValidator(validators.RegexValidator):
    regex = r'^[\w.@+-;]+\Z'


# Create your models here.
class MyUser(AbstractUser):
    username = CICharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_/; only.'),
        validators=[MyUnicodeUsernameValidator()],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
