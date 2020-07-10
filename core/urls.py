from django.urls import path
from .views import AboutView, Ajax2dView, DashboardHomeView, Ajax3dView


urlpatterns = [
    path('', DashboardHomeView.as_view(), name='home'),
    path('', DashboardHomeView.as_view(), name='dashboard_home'),
    path('about/', AboutView.as_view(), name='about'),
    path('dashboard/ajax/2d/', Ajax2dView.as_view(), name='dashboard_ajax_2d'),
    path('dashboard/ajax/3d/', Ajax3dView.as_view(), name='dashboard_ajax_3d'),
]
