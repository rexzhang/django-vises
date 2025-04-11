from enum import StrEnum, auto

from django.conf import settings


class DeployStage(StrEnum):
    UNKNOW = auto()
    LOCAL = auto()
    DEV = auto()
    UAT = auto()
    PRD = auto()


# Example
# from pydantic_settings import BaseSettings, SettingsConfigDict
#
# class DeployEnv(BaseSettings):
#     model_config = SettingsConfigDict(
#         env_prefix="POJ_",
#         env_file=".env",
#         env_file_encoding="utf-8",
#         extra="ignore",
#     )
#
#     DEPLOY_STAGE: str = DeployStage.UNKNOW
#     SENTRY_DSN: str = ""
#
#     ALLOWED_HOST: str = "localhost"


def template_context_processors(request):
    return {"DEPLOY_STAGE": settings.DEPLOY_ENV.DEPLOY_STAGE}
