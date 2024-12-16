from django.urls import path
from .views import push_result, pull_commands

urlpatterns = [
    path("pull", pull_commands, name="pull_commands"),
    path("result", push_result, name="push_result"),
]
