from django.db import models

class Agent(models.Model):
    agent_id = models.CharField(max_length=36, primary_key=True)
    last_heard = models.DateTimeField()
    host = models.GenericIPAddressField(default="127.0.0.1")


class Command(models.Model):
    agent_id = models.ForeignKey(to=Agent, on_delete=models.CASCADE)
    cmd_txt = models.CharField(max_length=1024)