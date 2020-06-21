from django.urls import path
from user.views import AgentView


urlpatterns = [
    path('', AgentView.as_view(), name='agent_list'),
]

