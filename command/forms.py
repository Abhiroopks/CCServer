from django import forms
from command.models import Agent, COMMAND_TYPES


class CommandForm(forms.Form):
    agent_id = forms.ModelChoiceField(
        queryset=Agent.objects.all(), to_field_name="id", empty_label=None
    )
    cmd_type = forms.ChoiceField(choices=COMMAND_TYPES)
    cmd_args = forms.CharField(max_length=1024)


class DeleteAgentForm(forms.Form):
    agent_id = forms.ModelChoiceField(
        queryset=Agent.objects.all(), to_field_name="id", empty_label=None
    )
