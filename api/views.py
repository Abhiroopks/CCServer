import json
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from command.models import Agent, Command, StatusTypes

@api_view(['POST'])
def push_result(request):
    """
    Updates the status of a command and its output.

    The request body should contain a JSON object with the following key-value pairs:
    - cmd_id: The id of the command to update.
    - output: The output of the command.
    - error: The output of the command if it failed.

    Returns an HTTP 204 if successful, or an HTTP 404 if the command ID is not recognized.
    """
    print(request.body)
    data: dict = json.loads(request.body)
    cmd_id = data.get("cmd_id")
    output = data.get("output")
    error = data.get("error")

    try:
        command = Command.objects.get(id=cmd_id)
        command.output = output
        command.error = error
        if command.error:
            command.status = StatusTypes.FAIL
        else:
            command.status = StatusTypes.SUCCESS
        command.save()
    except Command.DoesNotExist:
        raise NotFound(detail="Unrecognized command ID")

    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(["GET"])
def pull_commands(request) -> Response:
    """
    Returns a list of unexecuted commands for the agent with the given id.
    
    The request body should contain a JSON object with the following key-value pairs:
    - agent_id: The id of the agent.
    
    The response will be a JSON object with the following key-value pairs:
    - id: The id of a command.
    - cmd_type: The type of the command.
    - cmd_args: The arguments of the command.
    
    The response will be a list of such objects, one for each unexecuted command.
    """
    data: dict = json.loads(request.body)
    agent_id = data.get("agent_id")

    try:
        agent = Agent.objects.get(id=agent_id)
        agent.last_heard = timezone.now()
        agent.save()
    except Agent.DoesNotExist:
        agent = Agent(id=agent_id, last_heard=timezone.now(), host=get_client_ip(request))
        agent.save()

    cmds = Command.objects.filter(agent_id=agent_id, sent=False)
    cmd_list = []
    for cmd in cmds:
        cmd.sent = True
        cmd.save()
        cmd_list.append({
            "id": cmd.id,
            "cmd_type": cmd.cmd_type,
            "cmd_args": cmd.cmd_args
        }) 

    return Response(cmd_list, status=status.HTTP_200_OK, content_type="application/json")


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip