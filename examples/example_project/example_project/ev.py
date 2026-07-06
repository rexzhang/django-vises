from pathlib import Path

from dataclass_wizard import EnvWizard

from django_vises.django_settings.env_var import EnvVarAbc


class EnvVar(EnvVarAbc):
    class _(EnvWizard.Meta):
        env_file = Path("example.env")

    pass


EV = EnvVar()
