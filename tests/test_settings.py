from django_vises.vises.settings import parser_database_uri


def test_parser_database_uri():
    assert parser_database_uri("sqlite://") == {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "db.sqlite3",
    }

    assert parser_database_uri("sqlite:///data/db.sqlite3") == {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "/data/db.sqlite3",
    }

    assert parser_database_uri("postgresql://user:password@localhost:5432/db") == {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "db",
        "USER": "user",
        "PASSWORD": "password",
        "HOST": "localhost",
        "PORT": 5432,
    }
