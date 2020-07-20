""" urls of the chat module """
from django.urls import path
from .views import ChatListView, ChatDetailView, ChatNewMessageView, \
    ChatAjaxView, ChatUserDetailView


urlpatterns = [
    path('', ChatListView.as_view(), name='chat_list'),
    # path('index/', views.index, name='index'),
    # path('room/<str:room_name>/', views.room, name='room'),
    path('<int:pk>/', ChatDetailView.as_view(), name='chat_detail'),
    path('user/<int:user_pk>/', ChatUserDetailView.as_view(), name='chat_user_detail'),
    path(
        '<int:pk>/new/', ChatNewMessageView.as_view(), name='chat_new_message'
        ),
    path('ajax/<int:pk>/', ChatAjaxView.as_view(), name='chat_ajax_detail'),
]
