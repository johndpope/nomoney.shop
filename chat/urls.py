from django.urls import path
from .views import ChatListView, ChatDetailView, ChatNewMessageView, \
    ChatCreateView, ChatAjaxView, ChatAjaxStatusView, ChatUserDetailView
#from . import views

urlpatterns = [
    path('', ChatListView.as_view(), name='chat_list'),
    #path('index/', views.index, name='index'),
    #path('room/<str:room_name>/', views.room, name='room'),
    path('new/', ChatCreateView.as_view(), name='chat_create'),
    path('<int:pk>/', ChatDetailView.as_view(), name='chat_detail'),
    path('user/<int:user_pk>/', ChatUserDetailView.as_view(), name='chat_user_detail'),
    path(
        '<int:pk>/new/', ChatNewMessageView.as_view(), name='chat_new_message'
        ),
    path('ajax/<int:pk>/', ChatAjaxView.as_view(), name='chat_ajax_detail'),
    path('ajax/<int:pk>/status/', ChatAjaxStatusView.as_view(), name='chat_ajax_status'),
]
