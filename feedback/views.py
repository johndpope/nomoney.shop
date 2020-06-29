from django.urls.base import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, CreateView, UpdateView,\
    FormView
from .models import UserFeedback, PushFeedback
from .forms import FeedbackCreateForm


class FeedbackListView(TemplateView):
    template_name = 'feedback/feedback_list.html'

    def get_context_data(self, **kwargs):
        context = TemplateView.get_context_data(self, **kwargs)
        context['user_given'] = []
        #=======================================================================
        # context['user_taken']
        # context['pushs_given']
        # context['pushs_taken']
        #=======================================================================
        return context


"""
class FeedbackCreateView(CreateView):
    model = None
    type_ = None
    fields = ['score', 'subject', 'text', 'push']
    template_name = 'feedback/feedback_form.html'

    def setup(self, request, *args, **kwargs):
        self.type_ = kwargs.get('type')
        self.model = {
                'user': UserFeedback, 'push': PushFeedback
            }.get(self.type_)
        CreateView.setup(self, request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = CreateView.get_form(self, form_class=form_class)
        form.instance.creator = self.request.user
        return form

    def get_success_url(self):
        return reverse('feedback_detail', args=(self.type_, self.object.pk,))
"""

class FeedbackDetailView(DetailView):
    model = None
    type_ = None
    template_name = 'feedback/feedback_detail.html'

    def setup(self, request, *args, **kwargs):
        self.type_ = kwargs.get('type')
        self.model = {'user': UserFeedback, 'push': PushFeedback}.get(self.type_)
        DetailView.setup(self, request, *args, **kwargs)


class FeedbackUpdateView(UpdateView):
    model = None
    type_ = None
    template_name = 'feedback/feedback_detail.html'

    def setup(self, request, *args, **kwargs):
        self.type_ = kwargs.get('type')
        self.model = {'user': UserFeedback, 'push': PushFeedback}.get(self.type_)
        UpdateView.setup(self, request, *args, **kwargs)


class FeedbackDeleteView(DeleteView):
    model = None
    type_ = None
    template_name = 'feedback/feedback_detail.html'

    def setup(self, request, *args, **kwargs):
        self.type_ = kwargs.get('type')
        self.model = {'user': UserFeedback, 'push': PushFeedback}.get(self.type_)
        DeleteView.setup(self, request, *args, **kwargs)
