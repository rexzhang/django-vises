from pathlib import Path
from typing import Any
from urllib.parse import urlparse

SQLITE_FILE_NAME = "db.sqlite3"


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
