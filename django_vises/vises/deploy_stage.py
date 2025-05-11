from enum import StrEnum, auto

from django.conf import settings

"""需要在 settings.py 中初始化 DEPLOY_STAGE, 后续均使用这个值
"""


class DeployStage(StrEnum):
    UNKNOW = auto()
    LOCAL = auto()
    DEV = auto()
    UAT = auto()
    PRD = auto()


def template_context_processors(request):
    return {"DEPLOY_STAGE": settings.DEPLOY_STAGE}
