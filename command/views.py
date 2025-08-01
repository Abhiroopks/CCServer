from django.http import HttpResponse
from django.shortcuts import render
from command.models import Agent, Command
from command.forms import CommandForm, DeleteAgentForm

import json


def args_to_json(args: str) -> str:
    """
    Parses a string consisting of space-separated words and returns a JSON-serialized list of the words.
    """
    return json.dumps(args.split(" "))


def agents(request) -> HttpResponse:
    if request.method == "POST":
        if "cmd_form" in request.POST:
            form = CommandForm(request.POST)
            if form.is_valid():
                new_cmd = Command()
                new_cmd.cmd_type = form.cleaned_data.get("cmd_type")
                new_cmd.cmd_args = args_to_json(form.cleaned_data.get("cmd_args"))
                new_cmd.agent_id = form.cleaned_data.get("agent_id")
                new_cmd.save()
        if "delete_agent_form" in request.POST:
            form = DeleteAgentForm(request.POST)
            if form.is_valid():
                form.cleaned_data.get("agent_id").delete()

    context = {"agents": list(Agent.objects.all())}

    return render(request=request, template_name="command/agents.html", context=context)


def commands(request):
    if request.method == "POST":
        pass

    context = {"commands": list(Command.objects.all())}

    return render(
        request=request, template_name="command/commands.html", context=context
    )


