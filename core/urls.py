""" urls for core module - these are the root urls """
from django.urls import path
from .views import AboutView, DashboardHomeView, DonateView, TermsView, ImpressumView


urlpatterns = [
    path('', DashboardHomeView.as_view(), name='home'),
    path('', DashboardHomeView.as_view(), name='dashboard_home'),
    path('about/', AboutView.as_view(), name='about'),
    path('terms-and-conditions/', TermsView.as_view(), name='terms'),
    path('impressum/', ImpressumView.as_view(), name='impressum'),
    path('donate/', DonateView.as_view(), name='donate'),
    path('spende/', AboutView.as_view()),
]
