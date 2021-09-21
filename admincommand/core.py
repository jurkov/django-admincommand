import contextlib
import logging
from importlib import import_module

from django.conf import settings
from django.core import management
from django.core.management.base import CommandError
from io import StringIO

from admincommand.models import AdminCommand

schedule = None

# Cache variable to store runnable commands configuration
_command_configs = {}
output = StringIO()


def get_admin_commands():
    if _command_configs:
        return _command_configs

    for app_module_path in settings.INSTALLED_APPS:
        try:
            admin_commands_path = f"{app_module_path}.admin"
            module = import_module(admin_commands_path)
        except ImportError:
            pass
        else:
            admincommands = getattr(module, 'ADMIN_COMMAND_LIST', [])
            for command_name in admincommands:
                if command_name != "admin_command":
                    command_config = AdminCommand(command_name)
                    _command_configs[command_name] = command_config

    return _command_configs


def call_command(command_name, user_pk, args=None, kwargs=None):
    """
    Call command and store output
    """
    # user = User.objects.get(pk=user_pk) useless ?
    kwargs = kwargs or {}
    args = args or []
    output = StringIO()
    kwargs["stdout"] = output
    management.call_command(command_name, *args, **kwargs)
    return output.getvalue()


@contextlib.contextmanager
def monkeypatched(object, name, patch):
    """
    Temporarily monkeypatches an object.
    """

    pre_patched_value = getattr(object, name)
    setattr(object, name, patch)
    yield object
    setattr(object, name, pre_patched_value)


def getMessage(self):
    msg = str(self.msg)
    if self.args:
        msg = msg % self.args
    output.write(msg + "<br>")
    return msg


def run_command(command_config, validated_form, user):
    kwargs = {}
    if hasattr(command_config, "get_command_arguments"):
        args = command_config.get_command_arguments(validated_form, user)
    else:
        args = []

    if command_config.asynchronous:
        if not callable(schedule):
            return "This task is asynchronous but django-async is not installed"
        task = schedule(call_command, [command_config.name, user.pk, args, kwargs])
        return task

    # Synchronous call
    # Change stdout to a StringIO to be able to retrieve output and display it to the admin
    # TODO put back here legacy code with settings if needed

    with monkeypatched(logging.LogRecord, "getMessage", getMessage):
        try:
            management.call_command(command_config.name, *args, **kwargs)
        except CommandError as error:
            return error

    value = output.getvalue()
    output.seek(0)
    output.truncate(0)
    return value
