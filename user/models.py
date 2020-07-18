""" models for user module """
from statistics import mean
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.db import models
from chat.models import Chat
from listing.models import ListingStatus
from category.models import Category
from _collections import defaultdict
from config.settings import LOGGER


def image_path(instance, filename):
    """
    :returns: str path where to save the user image
    """
    suffix = filename.split('.')[-1]
    return 'user/{}/avatar.{}'.format(instance.pk, suffix)


class UserConfig(models.Model):
    """ class for saving additional user configuration """
    hint_step = models.PositiveSmallIntegerField(default=0)


class User(AbstractUser):
    """ The user is the central object

    username, first_name, last_name, email, is_staff, is_active, date_joined
    REQUIRED_FIELDS = ['email']
    """
    config = models.OneToOneField(
        UserConfig,
        on_delete=models.CASCADE,
        null=True,
        verbose_name=_('config'),
        )
    image = models.ImageField(
        blank=True,
        upload_to=image_path,
        verbose_name=_('image'),
        )
    description = models.TextField(
        blank=True,
        verbose_name=_('description'),
        )
    invisible = models.BooleanField(default=False)

    @property
    def chats(self):
        """ Chats of this user
        :returns: QuerySet(Chat)
        """
        lobby = [Chat.get_lobby().pk]
        user_chats = [chat.pk for chat in self.chat_set.all()]
        market_chats = [market.chat.pk for market in self.markets]
        pks = set(lobby + user_chats + market_chats)
        return Chat.objects.filter(pk__in=pks)

    @property
    def locations(self):
        """ Locations of this user
        :returns: QuerySet(Location)
        """
        return self.location_set.all()

    @property
    def other_users(self):
        """ All users except self
        :returns: QuerySet(User)
        """
        return self.__class__.objects.exclude(pk=self.pk)

    @property
    def pushs(self):
        """ Pushs of this user that are not marked as DELETED
        :returns: QuerySet(Push)
        """
        return self.push_set.exclude(status=ListingStatus.DELETED)

    @property
    def pulls(self):
        """ Pulls of this user that are not marked as DELETED
        :returns: QuerySet(Pull)
        """
        return self.pull_set.exclude(status=ListingStatus.DELETED)

    @property
    def markets(self):
        """ Markets of this user
        :returns: QuerySet(Market)
        """
        return self.market_set.all()

    @property
    def listings(self):
        """ All pushs and pulls of this user
        :returns: list(Pushs+Pulls)
        """
        return list(self.pushs) + list(self.pulls)

    @property
    def score(self):
        """ The score is calculated from previous taken userfeedback
        self.taken_feedbacks.aggregate(Avg('score'))['score__avg']
        :returns: int(score) or None
        """
        scores = []
        for feedback in self.feedback_for.all():
            if feedback.score:
                scores.append(feedback.score)
        if scores:
            return mean(scores)
        return None

    def get_unseen_messages(self):
        """ All unseen messages of this user
        :returns: QuerySet(ChatMessage)
        """
        return self.unseen_messages.all()

    def get_unseen_by_chat(self):
        """ All unseen messages of this user
        :returns: dict{chat.pk: [chat.unseen_messages]}
        """
        unseen_messages = defaultdict(list)
        for message in self.get_unseen_messages():
            unseen_messages[message.chat.pk].append(message)
        return unseen_messages

    @property
    def open_feedback(self):
        """ All open feedback of this user (user + push)
        :returns: list(open_userfeedback + open_pushfeedback)
        """
        return list(self.userfeedback_set.filter(status=0)) + \
            list(self.pushfeedback_set.filter(status=0))

    @property
    def deals(self):
        """ All deals of this user and sets the deal.pov_user to self
        :returns: QuerySet(Deal)
        """
        deals = self.user1_deals.all().union(self.user2_deals.all())
        for deal in deals:
            deal.set_pov(self)
        return deals

    def get_chat_with(self, *users):
        """ All chats of this user
        :returns: QuerySet(Chat)
        """
        return Chat.by_users(self, *users, create=True)

    def objects_to_prove(self):
        """ All categories to approve if user is_staff
        :returns: QuerySet(Category) or None
        """
        if self.is_staff:
            objects = {}
            objects['categories'] = Category.get_unproved()
            return objects
        return None

    def save(self, *args, **kwargs):  # pylint: disable=signature-differs
        log_string = 'User {}: username={}'.format(
            'updated' if self.pk else 'created',
            str(self.username),
            )
        LOGGER.info(log_string)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username or self.first_name + ' ' + self.last_name

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')


@receiver(pre_save, sender=User)
# pylint: disable=unused-argument
def create_user_config(sender, instance, **kwargs):
    """ create UserConfig when creating user
    Maybe it would be better to use User.save method if possible
    """
    instance.config = UserConfig.objects.create()
