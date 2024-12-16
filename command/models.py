from django.db import models
from django.utils.translation import gettext_lazy as _


class CommandTypes(models.TextChoices):
    LS = "ls", _("List Directory Contents")


class StatusTypes(models.TextChoices):
    UNKNOWN = "unknown", _("Unknown")
    SUCCESS = "success", _("Success")
    FAIL = "fail", _("Fail")


class Agent(models.Model):
    id = models.TextField(max_length=32, primary_key=True, default="abc123")
    last_heard = models.DateTimeField()
    host = models.GenericIPAddressField(default="127.0.0.1")


class Command(models.Model):
    agent_id = models.ForeignKey(to=Agent, on_delete=models.CASCADE)
    cmd_type = models.CharField(
        max_length=32, choices=CommandTypes.choices, verbose_name="Command Type"
    )
    ##
    # Command Args will be a JSON-serialized list.
    # Making sense of these will depend on the command type.
    cmd_args = models.CharField(max_length=1024, verbose_name="Command Arguments")
    sent = models.BooleanField(default=False)
    status = models.CharField(
        max_length=16,
        choices=StatusTypes.choices,
        verbose_name="Command Status",
        default=StatusTypes.UNKNOWN,
    )
    output = models.CharField(max_length=1024, verbose_name="Command Output")
    error = models.CharField(max_length=1024, verbose_name="Command Error")
