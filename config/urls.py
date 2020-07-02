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
from django.conf.urls.static import static
from django.urls import include, path
from user.views import AgentView
from config import settings
from django.views.i18n import JavaScriptCatalog


urlpatterns = [

    path('agent/', AgentView.as_view(), name='agent_list'),

    path('', include('dashboard.urls')),
    path('bid/', include('bid.urls')),
    path('user/', include('user.urls')),
    path('category/', include('category.urls')),
    path('listing/', include('listing.urls')),
    path('search/', include('search.urls')),
    path('chat/', include('chat.urls')),
    path('deal/', include('deal.urls')),
    path('guild/', include('guild.urls')),
    path('feedback/', include('feedback.urls')),

    path('', include('pwa.urls')),
    path('admin/', admin.site.urls),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
