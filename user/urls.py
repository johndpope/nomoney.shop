""" urls for the user module (/user/*) """
from django.urls import path
from django.urls.conf import include
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from user.views import UserListView, UserCreateView, UserUpdateView, \
    UserDetailView, UserSettingsView, UserLoginView
from config import settings


urlpatterns = [
    path('', UserListView.as_view(), name='user_list'),
    path('new/', UserCreateView.as_view(), name='user_create'),
    path('<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('update/', UserUpdateView.as_view(), name='user_update'),
    path('settings/', UserSettingsView.as_view(), name='user_settings'),
    path('pw/', PasswordChangeView.as_view(template_name='user/user_form.html'
                                           ), name='user_pw'),

    path('login/', UserLoginView.as_view(), name='user_login'),

    path('logout/', LogoutView.as_view(), name='user_logout'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
