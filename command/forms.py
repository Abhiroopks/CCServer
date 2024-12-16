from django import forms
from command.models import Agent, CommandTypes


class CommandForm(forms.Form):
    agent_id = forms.ModelChoiceField(
        queryset=Agent.objects.all(), to_field_name="id", empty_label=None
    )
    cmd_type = forms.ChoiceField(choices=CommandTypes.choices)
    cmd_args = forms.CharField(max_length=1024)


class DeleteAgentForm(forms.Form):
    agent_id = forms.ModelChoiceField(
        queryset=Agent.objects.all(), to_field_name="id", empty_label=None
    )
