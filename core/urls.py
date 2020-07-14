from django.urls import path
from .views import AboutView, Ajax2dView, DashboardHomeView, Ajax3dView, \
    DonateView, TermsView, ImpressumView


urlpatterns = [
    path('', DashboardHomeView.as_view(), name='home'),
    path('', DashboardHomeView.as_view(), name='dashboard_home'),
    path('about/', AboutView.as_view(), name='about'),
    path('terms-and-conditions/', TermsView.as_view(), name='terms'),
    path('impressum/', ImpressumView.as_view(), name='impressum'),
    path('donate/', DonateView.as_view(), name='donate'),
    path('spende/', AboutView.as_view()),
    path('dashboard/ajax/2d/', Ajax2dView.as_view(), name='dashboard_ajax_2d'),
    path('dashboard/ajax/3d/', Ajax3dView.as_view(), name='dashboard_ajax_3d'),
]
