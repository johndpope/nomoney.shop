from operator import attrgetter
from itertools import chain
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db.models import Avg
from django.contrib.auth.models import AbstractUser
from django.db import models
from chat.models import Chat
from feedback.models import PushFeedback
from statistics import mean


def image_path(instance, filename):
    suffix = filename.split('.')[-1]
    return 'user/{}/avatar.{}'.format(instance.pk, suffix)


class UserConfig(models.Model):
    hint_step = models.PositiveSmallIntegerField(default=0)


class User(AbstractUser):
    """
    first_name, last_name, email, is_staff, is_active, date_joined
    REQUIRED_FIELDS = ['email']
    """
    config = models.OneToOneField(UserConfig, on_delete=models.CASCADE, null=True)
    image = models.ImageField(blank=True, upload_to=image_path)
    beta_user = models.BooleanField(default=False)
    test = models.BooleanField(default=False)
    description = models.TextField(blank=True)

    @property
    def locations(self):
        return self.location_set.all()

    @property
    def other_users(self):
        return self.__class__.objects.exclude(pk=self.pk)

    @property
    def pushs(self):
        return self.push_set.all()

    @property
    def pulls(self):
        return self.pull_set.all()

    @property
    def guilds(self):
        return self.guild_set.all()

    @property
    def listings(self):
        """ returns list of listings (pushs and pulls) """
        return list(self.pushs) + list(self.pulls)

    @property
    def bids(self):
        return sorted(
            {*self.bids_sent.all(), *self.bids_received.all()},
            key=lambda x: x.datetime
            )

#===============================================================================
#     @property
#     def given_feedbacks(self): # taken
#         user_feedbacks = self.userfeedback_set.all()
#         push_feedbacks = PushFeedback.given_by_user(self)
#         return sorted(
#             chain(user_feedbacks, push_feedbacks),
#             key=attrgetter('created'),
#             reverse=True
#             )
# 
#     @property
#     def taken_feedbacks(self):
#         user_feedbacks = self.feedback_for.all()
#         push_feedbacks = PushFeedback.taken_by_user(self)
#         return sorted(
#             chain(user_feedbacks, push_feedbacks),
#             key=attrgetter('created'),
#             reverse=True
#             )
#===============================================================================

    @property
    def score(self):
        """ self.taken_feedbacks.aggregate(Avg('score'))['score__avg'] """
        feedback = self.feedback_for.all()
        if feedback:
            return mean((x.score for x in feedback if x.score is not None))

    @property
    def open_feedback(self):
        return list(self.userfeedback_set.filter(status=0)) + \
            list(self.pushfeedback_set.filter(status=0))

    @property
    def deals(self):
        deals = self.user1_deals.all().union(self.user2_deals.all())
        for deal in deals:
            deal.set_pov(self)
        return deals

    def get_chat_with(self, *users):
        return Chat.by_users(self, *users, create=True)

    def __str__(self):
        return self.username or self.first_name + ' ' + self.last_name


@receiver(pre_save, sender=User)
def create_user_config(sender, instance, **kwargs):
    instance.config = UserConfig.objects.create()
