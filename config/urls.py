"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.views.generic.base import TemplateView, RedirectView
from user.views import AgentView
from django.urls.base import reverse, reverse_lazy
from django.conf import settings
from django.urls import include, path


urlpatterns = [
    path(
        '', RedirectView.as_view(url=reverse_lazy('dashboard_home')), name='home'
        ),

    path('agent/', AgentView.as_view(), name='agent_list'),

    path('dashboard/', include('dashboard.urls')),
    path('bid/', include('bid.urls')),
    path('user/', include('user.urls')),
    path('category/', include('category.urls')),
    path('listing/', include('listing.urls')),
    path('search/', include('search.urls')),
    path('chat/', include('chat.urls')),
    path('deal/', include('deal.urls')),
    path('guild/', include('guild.urls')),

    path('admin/', admin.site.urls),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns