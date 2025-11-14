from dataclasses import dataclass, field
from uuid import uuid4

from django_vises.deploy.deploy_stage import DeployStage


@dataclass
class EnvVarAbc:
    """settings.py 实例化为 EV
    在 settings 之外的地方通过 settings.EV 的方式使用, 因为这个实例的变量名是不可控的
    """

    # 部署环境
    DEPLOY_STAGE: str = DeployStage.UNKNOW
    TZ: str = "UTC"

    # 安全相关
    ALLOWED_HOSTS: list[str] = field(default_factory=lambda: ["*"])
    SECRET_KEY: str = f"django-secure-key-{uuid4().hex}"
    CSRF_TRUSTED_ORIGINS: list[str] = field(
        default_factory=list
    )  # 一般情况可以用SECURE_PROXY_SSL_HEADER 解决

    # 调试相关
    DEBUG: bool = False
    SENTRY_DSN: str = ""

    # 资源信息
    DATABASE_URI: str = (
        "sqlite://"  # postgresql://username:password@loaclhost:5432/dbname
    )


# Example:
"""
# in `project.settings.py`

@dataclass
class EnvVar(EnvVarAbc, EnvWizard):
    class _(EnvWizard.Meta):
        env_file = True


EV = EnvVar()
"""
