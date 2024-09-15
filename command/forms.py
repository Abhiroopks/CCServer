from django import forms
from command.models import Agent


class CommandForm(forms.Form):
    agent_id = forms.ModelChoiceField(queryset=Agent.objects.all(), to_field_name="agent_id", empty_label=None)
    cmd_txt = forms.CharField()
