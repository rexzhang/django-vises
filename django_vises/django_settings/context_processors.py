from django.conf import settings


def env_var(request):
    return {"EV": settings.EV}
