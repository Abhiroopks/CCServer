from django.db import models

class Agent(models.Model):
    agent_id = models.CharField(max_length=36, primary_key=True)
    last_heard = models.DateTimeField()
    host = models.GenericIPAddressField(default="0.0.0.0")