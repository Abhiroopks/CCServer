from django.db import models

COMMAND_TYPES = [("ls", "List Files")]


class Agent(models.Model):
    id = models.TextField(max_length=32, primary_key=True, default="abc123")
    last_heard = models.DateTimeField()
    host = models.GenericIPAddressField(default="127.0.0.1")


class Command(models.Model):
    agent_id = models.ForeignKey(to=Agent, on_delete=models.CASCADE)
    cmd_type = models.CharField(
        max_length=32, choices=COMMAND_TYPES, verbose_name="Command Type"
    )
    ##
    # Command Args will be a JSON-serialized list.
    # Making sense of these will depend on the command type.
    cmd_args = models.CharField(max_length=1024, verbose_name="Command Arguments")
    sent = models.BooleanField(default=False)


class CommandResult(models.Model):
    cmd_id = models.ForeignKey(
        to=Command, on_delete=models.CASCADE, verbose_name="Command ID"
    )
    cmd_output = models.CharField(max_length=1024, verbose_name="Command Output")
    cmd_error = models.CharField(max_length=1024, verbose_name="Command Error")
