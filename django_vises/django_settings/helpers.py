from pathlib import Path
from typing import Any
from urllib.parse import ParseResult, urlparse

SQLITE_FILE_NAME = "db.sqlite3"


def _parser_sqlite_uri(
    data: ParseResult, base_dir: Path | None = None
) -> dict[str, Any]:
    if data.hostname:
        sqlite_file_name = data.hostname

    elif data.path:
        sqlite_file_name = data.path

    else:
        sqlite_file_name = SQLITE_FILE_NAME

    if base_dir:
        sqlite_file_name = base_dir.joinpath(sqlite_file_name).as_posix()

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

        case "postgresql" | "postgres":
            engine = "django.db.backends.postgresql"

        case _:
            raise ValueError(f"[{data.scheme}] is an unsupported database type")

    return {
        "ENGINE": engine,
        "HOST": data.hostname,
        "PORT": data.port,
        "NAME": data.path.lstrip("/"),
        "USER": data.username,
        "PASSWORD": data.password,
    }
