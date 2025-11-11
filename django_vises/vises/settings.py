from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from urllib.parse import ParseResult, urlparse
from uuid import uuid4

from .deploy_stage import DeployStage

SQLITE_FILE_NAME = "db.sqlite3"


@dataclass
class DeployEnvValueAbc:
    """不要在 settings.py 之外的地方使用这个类的实例, 因为这个实例的变量名是不可控的"""

    # 部署环境
    DEPLOY_STAGE: str = DeployStage.UNKNOW

    # 安全相关
    ALLOWED_HOSTS: list[str] = field(default_factory=list)
    SECRET_KEY: str = f"django-secret-key-{uuid4().hex}"
    CSRF_TRUSTED_ORIGINS: list[str] = field(
        default_factory=list
    )  # 一般情况可以用SECURE_PROXY_SSL_HEADER 解决

    # 调试相关
    DEBUG: bool = False
    SENTRY_DSN: str = ""

    # 资源信息
    DATABASE_URI: str = "sqlite://"


# Example:
#
# from dataclass_wizard import EnvWizard
#
# @dataclass
# class DeployEnvValue(DeployEnvValueAbc, EnvWizard):
#     class _(EnvWizard.Meta):
#         env_file = True
#
#     pass


def _parser_sqlite_uri(
    data: ParseResult, base_dir: Path | None = None
) -> dict[str, Any]:
    if data.path:
        sqlite_file_name = data.path

    else:
        if isinstance(base_dir, Path):
            sqlite_file_name = base_dir.joinpath(SQLITE_FILE_NAME).as_posix()
        else:
            sqlite_file_name = SQLITE_FILE_NAME

    return {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": sqlite_file_name,
    }


def parser_database_uri(uri: str, base_dir: Path | None = None) -> dict[str, Any]:
    """返回 Django settings DATABASES 字典"""
    data = urlparse(uri)
    match data.scheme:
        case "sqlite":
            return _parser_sqlite_uri(data, base_dir)

        case "postgresql":
            engine = "django.db.backends.postgresql"

        case _:
            raise

    return {
        "ENGINE": engine,
        "HOST": data.hostname,
        "PORT": data.port,
        "NAME": data.path.lstrip("/"),
        "USER": data.username,
        "PASSWORD": data.password,
    }
