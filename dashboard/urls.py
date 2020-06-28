from django.urls import path
from .views import Ajax2dView, DashboardHomeView, Ajax3dView


urlpatterns = [
    path('', DashboardHomeView.as_view(), name='dashboard_home'),
    path('ajax/2d/', Ajax2dView.as_view(), name='dashboard_ajax_2d'),
    path('ajax/3d/', Ajax3dView.as_view(), name='dashboard_ajax_3d'),
]

