from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from user.views import UserListView, UserCreateView, UserUpdateView, UserDetailView, AgentView

urlpatterns = [
    path('', UserListView.as_view(), name='user_list'),
    path('new/', UserCreateView.as_view(), name='user_create'),
    path('<int:pk>/update/', UserUpdateView.as_view(), name='user_update'),
    path('<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('<int:pk>/pw/', PasswordChangeView.as_view(template_name='user/user_form.html'), name='user_pw'),
    path('login/', LoginView.as_view(template_name='user/user_form.html'), name='user_login'),
    path('logout/', LogoutView.as_view(), name='user_logout'),
]

