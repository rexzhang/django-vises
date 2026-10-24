from pathlib import Path
from typing import Any
from urllib.parse import ParseResult, parse_qsl, urlparse

SQLITE_FILE_NAME = "db.sqlite3"

# query 小写键 -> Django DATABASES 顶层键; 这些是 Django 连接维护配置,
# 不是驱动 (libpq/psycopg) 参数, 留在 OPTIONS 会导致首次连接即失败
_DATABASES_TOP_LEVEL_KEYS: dict[str, str] = {
    "conn_max_age": "CONN_MAX_AGE",
    "conn_health_checks": "CONN_HEALTH_CHECKS",
    "disable_server_side_cursors": "DISABLE_SERVER_SIDE_CURSORS",
    "autocommit": "AUTOCOMMIT",
}


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


def _parser_service_sql_uri(data: ParseResult, engine: str) -> dict[str, Any]:
    """postgresql/mysql..."""
    return {
        "ENGINE": engine,
        "HOST": data.hostname,
        "PORT": data.port,
        "NAME": data.path.lstrip("/"),
        "USER": data.username,
        "PASSWORD": data.password,
    }


def _parser_options(query: str) -> dict[str, Any]:
    if not query:
        return {}

    data = parse_qsl(query)
    if not data:
        return {}

    result: dict[str, Any] = dict()
    for item in data:
        key, raw_value = item
        value: Any = raw_value

        # parser value
        if value.lower() == "true":
            value = True
        elif value.lower() == "false":
            value = False
        elif value.isdecimal():
            if "." in value:
                value = float(value)
            else:
                value = int(value)

        # parser key
        keys_chain = key.split(".")
        current_dict = result
        for key in keys_chain[:-1]:
            if key not in current_dict or not isinstance(current_dict[key], dict):
                current_dict[key] = {}

            current_dict = current_dict[key]

        final_key = keys_chain[-1]
        current_dict[final_key] = value

    return result


def parser_database_uri(uri: str, base_dir: Path | None = None) -> dict[str, Any]:
    """返回 Django settings DATABASES 字典

    query string 中的连接维护参数 (_DATABASES_TOP_LEVEL_KEYS) 映射为
    DATABASES 顶层键, 其余参数进入 OPTIONS (驱动参数)
    """
    data = urlparse(uri)
    match data.scheme:
        case "sqlite":
            result = _parser_sqlite_uri(data, base_dir)

        case "postgresql" | "postgres":
            result = _parser_service_sql_uri(data, "django.db.backends.postgresql")

        case _:
            raise ValueError(f"[{data.scheme}] is an unsupported database type")

    options = _parser_options(data.query)
    for query_key, setting_key in _DATABASES_TOP_LEVEL_KEYS.items():
        if query_key in options:
            result[setting_key] = options.pop(query_key)

    if options:
        result["OPTIONS"] = options

    return result
