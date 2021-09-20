import json
from django import forms
from dateutil.parser import parse as date_parse


class GenericCommandForm(forms.Form):
    command = None

    mapping_type = {
        bool: forms.CharField,
        str: forms.CharField,
        int: forms.IntegerField,
        float: forms.FloatField,
        json.loads: forms.JSONField,
        date_parse: forms.DateField,
    }

    def _get_form_field_based_on_type(self, type):
        return self.mapping_type.get(type, forms.BooleanField)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        default_actions = ("help", "version", "verbosity", "settings", "pythonpath", "traceback", "no_color")
        # TODO check what is the purpose of those arguments here, maybe needed only in case of full help display ?
        parser = self.command.create_parser("", None)
        # Example
        # {'const': True, 'help': None, 'option_strings': ['--run'], 'dest': 'run', 'required': False, 'nargs': 0,
        #  'choices': None, 'default': False, type': None, 'metavar': None}

        for option in parser._actions:
            if option.dest not in default_actions:
                form_callable = self._get_form_field_based_on_type(option.type)
                self.fields[option.dest] = form_callable(
                    initial=option.default, required=option.required, help_text=option.help
                )
