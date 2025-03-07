from django.urls import path
from django.views.generic.base import RedirectView

from . import views

urlpatterns = [
    path("", RedirectView.as_view(url="agents"), name="index"),
    path("agents", views.agents, name="agents"),
    path("commands", views.commands, name="commands"),
]
