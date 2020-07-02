from django.urls import path
from .views import GuildListView, GuildDetailView, GuildCreateView, \
    GuildUpdateView, GuildDeleteView


urlpatterns = [
    path('', GuildListView.as_view(), name='guild_list'),
    path('new/', GuildCreateView.as_view(), name='guild_create'),
    path('<int:pk>/', GuildDetailView.as_view(), name='guild_detail'),
    path('<int:pk>/update/', GuildUpdateView.as_view(), name='guild_update'),
    path('<int:pk>/delete/', GuildDeleteView.as_view(), name='guild_delete'),
]
