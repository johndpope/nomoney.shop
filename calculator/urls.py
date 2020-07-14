from django.urls import include, path
from .views import CalculatorView


urlpatterns = [
    path('', CalculatorView.as_view(), name='calculator'),

]
