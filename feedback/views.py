""" views for the feedback module """
from operator import attrgetter
from django.views.generic.base import TemplateView, View
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, UpdateView
from django import forms
from django.urls.base import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from listing.models import Push
from .models import UserFeedback, PushFeedback


class FeedbackContextMixin(TemplateView):
    """ dry """
    @staticmethod
    def get_feedback_by_user(user):
        """ fetch the feedback lists
        :returns: list[[UserFeedback.taken],[PushFeedback.taken],
                                    [UserFeedback.given],[PushFeedback.given]]
        """
        methods = (
            UserFeedback.taken_by_user,
            PushFeedback.taken_by_user,
            UserFeedback.given_by_user,
            PushFeedback.given_by_user
            )
        return [list(method_(user).exclude(status=0)) for method_ in methods]

    @classmethod
    def get_feedback(cls, user):
        """ sorts the objects from get_feedback_by_user and gives them back
        :returns: [feedback_given], [feedback_taken]
        """
        user_taken, push_taken, user_given, push_given = cls.get_feedback_by_user(user)
        return sorted((user_taken + push_taken), key=attrgetter('created'), reverse=True), \
            sorted((user_given + push_given), key=attrgetter('created'), reverse=True)

    def get_context_data(self, **kwargs):
        context = TemplateView.get_context_data(self, **kwargs)
        user = self.request.user
        if self.type == 'push':
            push = Push.objects.get(pk=self.pk_)
            context['push_feedback_taken'] = push.pushfeedback_set.exclude(status=0)
            context['push'] = push
        else:
            context['user_feedback_given'], context['user_feedback_taken'] = \
                self.get_feedback(user)
        context['user'] = user
        return context


class FeedbackTypeListView(FeedbackContextMixin, LoginRequiredMixin, TemplateView):
    """ List feedback objects of type for direct access """
    template_name = 'feedback/feedback_list.html'
    user = None
    type, pk_ = 2 * [None]

    def setup(self, request, *args, **kwargs):
        self.type = kwargs.get('type')
        self.pk_ = kwargs.get('pk')
        ListView.setup(self, request, *args, **kwargs)


class FeedbackListView(FeedbackContextMixin, LoginRequiredMixin, TemplateView):
    """ List feedback """
    template_name = 'feedback/feedback_list.html'


class FeedbackUpdateView(LoginRequiredMixin, UpdateView):
    """ UpdateView to update a feedback """
    model = None
    template_name = 'feedback/feedback_form.html'
    fields = ['score', 'subject', 'text']
    type_, deal = 2 * [None]

    def setup(self, request, *args, **kwargs):
        self.type_ = kwargs.get('type')
        self.model = {
            'user': UserFeedback,
            'push': PushFeedback,
            }.get(self.type_)
        self.deal = self.model.objects.get(pk=kwargs.get('pk')).deal
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


class FeedbackDetailDeleteBase(LoginRequiredMixin, View):
    """ Baseview for Feedback Detail and Delete View """
    model = None
    type_ = None
    template_name = 'feedback/feedback_detail.html'

    def setup(self, request, *args, **kwargs):
        self.type_ = kwargs.get('type')
        self.model = {'user': UserFeedback, 'push': PushFeedback}.get(self.type_)
        DetailView.setup(self, request, *args, **kwargs)


class FeedbackDetailView(FeedbackDetailDeleteBase, DetailView):
    """ DetailView of a single feedback """


class FeedbackDeleteView(FeedbackDetailDeleteBase, DeleteView):
    """ DeleteView to delete a feedback """
