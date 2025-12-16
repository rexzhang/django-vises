from dataclasses import dataclass

from dataclass_wizard import EnvWizard

from django_vises.django_settings.env_var import EnvVarAbc


@dataclass
class EnvVar(EnvVarAbc, EnvWizard):
    class _(EnvWizard.Meta):
        env_file = "examples/example_project/example.env"

    pass


EV = EnvVar()
