from pathlib import Path

import pytest

from django_vises.django_settings.helpers import parser_database_uri


def test_parser_database_uri():
    # sqlite ---
    # --- default
    assert parser_database_uri("sqlite://") == {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "db.sqlite3",
    }

    assert parser_database_uri("sqlite://", base_dir=Path("/data")) == {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "/data/db.sqlite3",
    }

    # --- match http hostname
    assert parser_database_uri("sqlite://db_v2.sqlite3") == {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "db_v2.sqlite3",
    }

    assert parser_database_uri("sqlite://db_v2.sqlite3", base_dir=Path("/data")) == {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "/data/db_v2.sqlite3",
    }

    # --- match http path
    assert parser_database_uri("sqlite:///data/db.sqlite3") == {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "/data/db.sqlite3",
    }

    assert parser_database_uri("sqlite:///data/db.sqlite3", base_dir=Path("/data")) == {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "/data/db.sqlite3",  # base_dir is ignored
    }

    # postgresql ---
    assert parser_database_uri("postgresql://user:password@localhost:5432/db") == {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "db",
        "USER": "user",
        "PASSWORD": "password",
        "HOST": "localhost",
        "PORT": 5432,
    }

    assert parser_database_uri("postgres://user:password@localhost:5432/db") == {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "db",
        "USER": "user",
        "PASSWORD": "password",
        "HOST": "localhost",
        "PORT": 5432,
    }

    # unknown
    pytest.raises(
        ValueError,
        parser_database_uri,
        "unknow://",
    )
