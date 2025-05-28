import ulid
from django.db import models
from django.utils.translation import gettext_lazy as _


class UlidField(models.CharField):
    description = _("Universally Unique Lexicographically Sortable Identifier")

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 26)
        kwargs.setdefault('editable', False)
        kwargs.setdefault('unique', True)
        kwargs.setdefault('blank', True)
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname)
        if not value:
            value = ulid.new().str
            setattr(model_instance, self.attname, value)
        return value

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        # Remove defaults so they don't clutter migrations
        if kwargs.get("max_length", None) == 26:
            del kwargs["max_length"]
        if kwargs.get("editable", None) is False:
            del kwargs["editable"]
        if kwargs.get("unique", None) is True:
            del kwargs["unique"]
        if kwargs.get("blank", None) is True:
            del kwargs["blank"]
        return name, path, args, kwargs
