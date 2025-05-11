from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from pydantic_settings import BaseSettings, SettingsConfigDict

from .deploy_stage import DeployStage

SQLITE_FILE_NAME = "db.sqlite3"


class DeployEnvValueAbc(BaseSettings):
    """不要在 settings.py 之外的地方使用这个类的实例, 因为这个实例的变量名是不可控的"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # 部署环境
    DEPLOY_STAGE: str = DeployStage.UNKNOW
    SENTRY_DSN: str = ""

    # 安全相关
    DEBUG: bool = False
    ALLOWED_HOSTS: list[str] = []

    # 资源信息
    DATABASE_URI: str = "sqlite"


def parser_database_uri(
    uri: str, base_dir: Path | None = None
) -> dict[str, Any] | None:
    """返回 Django settings DATABASES 字典"""
    if uri.startswith("sqlite"):
        if isinstance(base_dir, Path):
            sqlite_file_name = base_dir.joinpath(SQLITE_FILE_NAME)
        else:
            sqlite_file_name = SQLITE_FILE_NAME

        return {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": sqlite_file_name,
        }

    data = urlparse(uri)
    match data.scheme:
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
