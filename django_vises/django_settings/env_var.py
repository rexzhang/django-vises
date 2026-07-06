from dataclasses import dataclass, field
from uuid import uuid4

from django_vises.deploy.deploy_stage import DeployStage


@dataclass
class EnvVarAbc:
    """在 dj_project/ev.py 中被集成并实例化为 EV
    在 django 项目中以 from dj_project.ev import EV 的方式使用
    """

    # 部署环境
    DEPLOY_STAGE: str = DeployStage.PRD
    TZ: str = "UTC"

    # Django --- 默认值优先考虑使用 Django 默认值
    # --- 安全相关
    ALLOWED_HOSTS: list[str] = field(default_factory=list)  # dev 环境可以使用 [“*”]
    DEBUG: bool = False
    SECRET_KEY: str = f"django-secure-key-{uuid4().hex}"

    CSRF_TRUSTED_ORIGINS: list[str] = field(
        default_factory=list
    )  # 一般情况可以用 SECURE_PROXY_SSL_HEADER 解决

    # --- 数据库
    # examples:
    #   postgresql://username:password@loaclhost:5432/dbname?pool=true
    #   postgresql://username:password@loaclhost:5432/dbname?pool.min_size=1&pool.max_size=10
    #   sqlite://db.sqlite3?init_command=PRAGMA journal_mode=WAL;PRAGMA synchronous=NORMAL;
    DATABASE_URI: str = (
        "sqlite://db.sqlite3?init_command=PRAGMA journal_mode=WAL;PRAGMA synchronous=NORMAL;"
    )

    # --- Cache
    # - https://docs.djangoproject.com/zh-hans/5.2/topics/cache
    CACHES_DEAFULT_BACKEND: str = "django.core.cache.backends.dummy.DummyCache"
    CACHES_DEAFULT_LOCATION: str = ""

    CACHES_SESSION_BACKEND: str = "django.core.cache.backends.dummy.DummyCache"
    CACHES_SESSION_LOCATION: str = ""

    CACHES_CELERY_BACKEND: str = "django.core.cache.backends.dummy.DummyCache"
    CACHES_CELERY_LOCATION: str = ""

    # 异常捕获
    SENTRY_DSN: str = ""

    # logfire
    LOGFIRE_TOKEN: str = ""


# Example:
"""
# in `project.settings.py`

@dataclass
class EnvVar(EnvVarAbc, EnvWizard):
    class _(EnvWizard.Meta):
        env_file = True

    COUSTOM_VAR:str = "custom_var"

EV = EnvVar()
"""
