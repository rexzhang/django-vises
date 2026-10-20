from django.conf import settings
from django.http import HttpRequest

from django_vises.django_settings.env_var import EnvVarAbc


def env_vars(request: HttpRequest) -> dict[str, EnvVarAbc]:
    return {"EV": settings.EV}
