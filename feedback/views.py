from operator import attrgetter
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, UpdateView
from django import forms
from django.urls.base import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from user.models import User
from listing.models import Push
from .models import UserFeedback, PushFeedback


class FeedbackTypeListView(LoginRequiredMixin, TemplateView):
    template_name = 'feedback/feedback_list.html'
    user = None
    type, pk_ = 2 * [None]

    def setup(self, request, *args, **kwargs):
        self.type = kwargs.get('type')
        self.pk_ = kwargs.get('pk')
        ListView.setup(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = TemplateView.get_context_data(self, **kwargs)
        if self.type == 'push':
            push = Push.objects.get(pk=self.pk_)
            context['push_feedback_taken'] = push.pushfeedback_set.exclude(status=0)
            context['push'] = push
        elif self.type == 'user':
            user = self.request.user
            user_feedback_given = list(UserFeedback.given_by_user(user).exclude(status=0))
            push_feedback_given = list(PushFeedback.given_by_user(user).exclude(status=0))
            context['user_feedback_given'] = sorted((user_feedback_given + push_feedback_given), key=attrgetter('created'), reverse=True)

            user_feedback_taken = list(UserFeedback.taken_by_user(user).exclude(status=0))
            push_feedback_taken = list(PushFeedback.taken_by_user(user).exclude(status=0))
            context['user_feedback_taken'] = sorted((user_feedback_taken + push_feedback_taken), key=attrgetter('created'), reverse=True) #requestuser
        else:
            user = self.request.user
            user_feedback_given = list(UserFeedback.given_by_user(user).exclude(status=0))
            push_feedback_given = list(PushFeedback.given_by_user(user).exclude(status=0))
            context['user_feedback_given'] = sorted((user_feedback_given + push_feedback_given), key=attrgetter('created'), reverse=True)

            user_feedback_taken = list(UserFeedback.taken_by_user(user).exclude(status=0))
            push_feedback_taken = list(PushFeedback.taken_by_user(user).exclude(status=0))
            context['user_feedback_taken'] = sorted((user_feedback_taken + push_feedback_taken), key=attrgetter('created'), reverse=True) #requestuser
        return context



class FeedbackListView(LoginRequiredMixin, TemplateView):
    template_name = 'feedback/feedback_list.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = TemplateView.get_context_data(self, **kwargs)
        user_feedback_given = list(UserFeedback.given_by_user(user).exclude(status=0))
        push_feedback_given = list(PushFeedback.given_by_user(user).exclude(status=0))
        context['user_feedback_given'] = sorted((user_feedback_given + push_feedback_given), key=attrgetter('created'), reverse=True)

        user_feedback_taken = list(UserFeedback.taken_by_user(user).exclude(status=0))
        push_feedback_taken = list(PushFeedback.taken_by_user(user).exclude(status=0))
        context['user_feedback_taken'] = sorted((user_feedback_taken + push_feedback_taken), key=attrgetter('created'), reverse=True)

        context['user'] = user
        return context


class FeedbackDetailView(LoginRequiredMixin, DetailView):
    model = None
    type_ = None
    template_name = 'feedback/feedback_detail.html'
 
    def setup(self, request, *args, **kwargs):
        self.type_ = kwargs.get('type')
        self.model = {'user': UserFeedback, 'push': PushFeedback}.get(self.type_)
        DetailView.setup(self, request, *args, **kwargs)


class FeedbackUpdateView(LoginRequiredMixin, UpdateView):
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


class FeedbackDeleteView(LoginRequiredMixin, DeleteView):
    model = None
    type_ = None
    template_name = 'feedback/feedback_detail.html'

    def setup(self, request, *args, **kwargs):
        self.type_ = kwargs.get('type')
        self.model = {'user': UserFeedback, 'push': PushFeedback}.get(self.type_)
        DeleteView.setup(self, request, *args, **kwargs)
