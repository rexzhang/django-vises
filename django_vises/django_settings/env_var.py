from dataclasses import dataclass, field
from uuid import uuid4

from django_vises.deploy.deploy_stage import DeployStage


@dataclass
class EnvVarAbc:
    """不要在 settings.py 之外的地方使用这个类的实例, 因为这个实例的变量名是不可控的"""

    # 部署环境
    DEPLOY_STAGE: str = DeployStage.UNKNOW

    # 安全相关
    ALLOWED_HOSTS: list[str] = field(default_factory=list)
    SECRET_KEY: str = f"django-insecure-key-{uuid4().hex}"
    CSRF_TRUSTED_ORIGINS: list[str] = field(
        default_factory=list
    )  # 一般情况可以用SECURE_PROXY_SSL_HEADER 解决

    # 调试相关
    DEBUG: bool = False
    SENTRY_DSN: str = ""

    # 资源信息
    DATABASE_URI: str = "sqlite://"


# Example:
"""
# in `project.settings.py`

@dataclass
class EnvVar(EnvVarAbc, EnvWizard):
    class _(EnvWizard.Meta):
        env_file = True


EV = EnvVar()
"""
