from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("pull", views.pull_commands, name="pull_commands"),
]