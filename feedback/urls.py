from django.urls import path
from .views import FeedbackUpdateView, FeedbackDeleteView, FeedbackListView, \
    FeedbackTypeListView


urlpatterns = [
    path('', FeedbackListView.as_view(), name='feedback_list'),
    path('<slug:type>/<int:pk>/', FeedbackTypeListView.as_view(), name='feedback_detail'),
    path('<slug:type>/<int:pk>/update/', FeedbackUpdateView.as_view(), name='feedback_update'),
    path('<slug:type>/<int:pk>/delete/', FeedbackDeleteView.as_view(), name='feedback_delete'),
]
