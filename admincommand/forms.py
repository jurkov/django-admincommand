import json
from django import forms
from dateutil.parser import parse as date_parse


class GenericCommandForm(forms.Form):
    command = None

    mapping_type = {
        bool: forms.BooleanField,
        str: forms.CharField,
        int: forms.IntegerField,
        float: forms.FloatField,
        json.loads: forms.JSONField,
        date_parse: forms.DateField,
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.default_actions = (
            "help", "version", "verbosity", "settings", "pythonpath", "traceback", "no_color"
        )
        # TODO check what is the purpose of those arguments here, maybe needed only in case of full help display ?
        parser = self.command.create_parser("", None)
        # Example
        # {'const': True, 'help': None, 'option_strings': ['--run'], 'dest': 'run', 'required': False, 'nargs': 0,
        #  'choices': None, 'default': False, type': None, 'metavar': None}

        self._process_actions(parser._get_positional_actions(), forms.CharField)
        self._process_actions(parser._get_optional_actions(), forms.BooleanField)

    def _process_actions(self, actions, default_form):
        for action in actions:
            if action.dest not in self.default_actions:
                if action.choices:
                    form_callable = forms.ChoiceField
                    choices = {'choices': [(choice, choice) for choice in action.choices]}
                else:
                    form_callable = self.mapping_type.get(
                        action.type or type(action.default),
                        default_form
                    )
                    choices = {}

                self.fields[action.dest] = form_callable(
                    initial=action.default, required=action.required, help_text=action.help,
                    **choices
                )
