from django.http import HttpResponse
from django.shortcuts import render
from command.models import Agent

from django.utils import timezone


def pull_commands(request) -> HttpResponse:
    agent_id = request.GET["agent_id"]
    agent = Agent()

    agent.agent_id = agent_id
    agent.last_heard = timezone.now()
    agent.host = get_client_ip(request)
    
    agent.save()
    return HttpResponse(f"Hello agent {agent_id}.")


def index(request) -> HttpResponse:
    context = {"agents": list(Agent.objects.all())}
    return render(request=request, template_name="command/index.html", context=context)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip