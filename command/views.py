from django.http import HttpResponse
from django.shortcuts import render
from command.models import Agent, Command
from command.forms import CommandForm, DeleteAgentForm
from django.core import serializers

from django.utils import timezone

import json


def args_to_json(args: str) -> str:
    """
    Parses a string consisting of space-separated words and returns a JSON-serialized list of the words.
    """
    return json.dumps(args.split(" "))


def pull_commands(request) -> HttpResponse:
    ##
    # Update agent's last_heard if seen before
    # if not seen before, create the new agent
    agent_id = request.GET["agent_id"]

    try:
        agent = Agent.objects.get(id=agent_id)
        agent.last_heard = timezone.now()
        agent.save()
    except Agent.DoesNotExist:
        agent = Agent()
        agent.id = agent_id
        agent.last_heard = timezone.now()
        agent.host = get_client_ip(request)
        agent.save()

    ##
    # Fetch all commands for this agent to run
    cmds = Command.objects.filter(agent_id=agent_id).filter(sent=False)
    for cmd in cmds:
        cmd.sent = True
        cmd.save()

    return HttpResponse(serializers.serialize("json", cmds))


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


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip
