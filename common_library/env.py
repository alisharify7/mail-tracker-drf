from decouple import config, UndefinedValueError
from django.core.exceptions import ImproperlyConfigured


def required_env(varname, **kwargs):
    """
    DATABASE_URL = required_env('DATABASE_URL')
    """
    try:
        return config(varname, **kwargs)
    except UndefinedValueError:
        raise ImproperlyConfigured(
            f"Environment variable {varname!r} is required but not set."
        )
