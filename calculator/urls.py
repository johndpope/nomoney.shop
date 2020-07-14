from django.urls import include, path
from .views import CalculatorView, AjaxDirectDealsView, AjaxSpeculativeDealsView, AjaxTriangularDealsView


urlpatterns = [
    path('', CalculatorView.as_view(), name='calculator'),
    path('ajax/deals/direct/', AjaxDirectDealsView.as_view(), name='ajax_deals_direct'),
    path('ajax/deals/triangular/', AjaxTriangularDealsView.as_view(), name='ajax_deals_triangular'),
    path('ajax/deals/speculative/', AjaxSpeculativeDealsView.as_view(), name='ajax_deals_speculative'),
]
