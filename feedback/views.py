from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, UpdateView,\
    FormView
from .models import UserFeedback, PushFeedback
from .forms import PushFeedbackUpdateForm, UserFeedbackUpdateForm
from django import forms
from django.urls.base import reverse

class FeedbackListView(TemplateView):
    template_name = 'feedback/feedback_list.html'

    def get_context_data(self, **kwargs):
        context = TemplateView.get_context_data(self, **kwargs)
        context['user_feedback_open'] = self.request.user.userfeedback_set.filter(status=0)
        context['push_feedback_open'] = self.request.user.pushfeedback_set.filter(status=0)
        context['user_feedback'] = self.request.user.userfeedback_set.exclude(status=0)
        context['push_feedback'] = self.request.user.pushfeedback_set.exclude(status=0)
        return context


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
    template_name = 'feedback/feedback_form.html'
    fields = ['score', 'subject', 'text']

    def setup(self, request, *args, **kwargs):
        self.type_ = kwargs.get('type')
        self.model = {
            'user': UserFeedback,
            'push': PushFeedback,
            }.get(self.type_)
        self.deal = self.model.objects.get(pk=kwargs.get('pk')).deal
        #self.deal.set_pov(self.request.user)
        UpdateView.setup(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = UpdateView.get_context_data(self, **kwargs)
        context['deal'] = self.deal
        return context

    def get_form(self, form_class=None):
        form = UpdateView.get_form(self, form_class=form_class)
        form.fields['score'].widget = forms.HiddenInput()
        return form

    def form_valid(self, form):
        response = UpdateView.form_valid(self, form)
        self.get_object().set_sent()
        return response

    def get_success_url(self):
        return reverse('feedback_list')

    #===========================================================================
    # def get_context_data(self, **kwargs):
    #     context = FormView.get_context_data(self, **kwargs)
    #     context['deal'] = 
    #===========================================================================


class FeedbackDeleteView(DeleteView):
    model = None
    type_ = None
    template_name = 'feedback/feedback_detail.html'

    def setup(self, request, *args, **kwargs):
        self.type_ = kwargs.get('type')
        self.model = {'user': UserFeedback, 'push': PushFeedback}.get(self.type_)
        DeleteView.setup(self, request, *args, **kwargs)
