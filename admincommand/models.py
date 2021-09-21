from django.db import models
from django.core.management import get_commands, load_command_class
from django.core.management.base import BaseCommand

from admincommand.forms import GenericCommandForm


class AdminCommand(models.Model):

    # TODO
    # asynchronous = False

    objects = None
    form = GenericCommandForm

    def __init__(self, name, *args, **kwargs):
        self.name = name
        super().__init__(*args, **kwargs)

    def get_help(self):
        if hasattr(self, "help"):
            return self.help
        return self.command().help

    def command(self):
        app_name = get_commands()[self.name]
        if isinstance(app_name, BaseCommand):
            # If the command is already loaded, use it directly.
            return app_name
        return load_command_class(app_name, self.name)

    def permission_codename(self):
        return f"can_run_command_{self.name}"

    @classmethod
    def all(cls):
        from . import core

        for runnable_command in core.get_admin_commands().values():
            yield runnable_command

    def get_command_arguments(self, validated_form, user):
        # TODO check why user was passed over here
        args = []
        for key, value in validated_form.cleaned_data.items():

            # Postional actions
            if validated_form.fields[key].required:
                args.append(value)

            # Optional actions
            else:
                if value is True:
                    args.append(f"--{key}")
                elif value:
                    args.append(f"--{key}={value}")

        return args
