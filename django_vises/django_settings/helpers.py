from pathlib import Path
from typing import Any
from urllib.parse import ParseResult, urlparse

SQLITE_FILE_NAME = "db.sqlite3"


def _parser_sqlite_uri(
    data: ParseResult, base_dir: Path | None = None
) -> dict[str, Any]:
    if data.path:
        sqlite_file_name = data.path

    elif data.hostname:
        sqlite_file_name = data.hostname

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
