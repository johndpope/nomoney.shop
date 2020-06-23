from django.urls import path
from .views import ChatListView, ChatDetailView, ChatNewMessageView, \
    ChatCreateView


urlpatterns = [
    path('', ChatListView.as_view(), name='chat_list'),
    path('new/', ChatCreateView.as_view(), name='chat_create'),
    path('<int:pk>/', ChatDetailView.as_view(), name='chat_detail'),
    path(
        '<int:pk>/new/', ChatNewMessageView.as_view(), name='chat_new_message'
        ),
]

