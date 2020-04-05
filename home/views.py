from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from listing.models import Pull, Category


class Home(TemplateView):
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):
        context = TemplateView.get_context_data(self, **kwargs)
        context['categories'] = sorted(Category.objects.all())
        return context

    #===========================================================================
    # def get(self, request, *args, **kwargs):
    #     response = ListView.get(self, request, *args, **kwargs)
    #     #import pdb; pdb.set_trace()  # <---------
    #     return response
    #===========================================================================

#===============================================================================
# class Home(ListView):
#     template_name = 'home/home.html'
#     model = Listing
#     context_object_name = 'listings'
#===============================================================================
