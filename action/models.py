""" models for the experience app

Experience is gained from doing actions

create actions from everywher like:

create_action(self.request.user, 'DAILY_VISIT')
or create_action(self.request.user, 1)
"""
from django.utils.translation import ngettext, gettext_lazy as _
from django.db import models
from django.utils.safestring import mark_safe
from user_messages import api
from config.settings import AUTH_USER_MODEL, LOGGER
from .task import DefaultTask, OneTimeTask, DailyTask
from .exp import Level  # Migrations error when removed

__all__ = ['create_action']


# TypeofTask(index, unique_name, title, exp, [min_level, max_level])
TASKS = [  # never change the index numbers, thei're db relevant !!!
    DailyTask(1, _('DAILY_VISIT'), 2),
    OneTimeTask(2, _('USER_CREATED'), 5),

    DefaultTask(3, _('PUSH_CREATED'), 5),
    OneTimeTask(4, _('FIRST_PUSH_CREATED'), 10),

    DefaultTask(5, _('PULL_CREATED'), 4),
    OneTimeTask(6, _('FIRST_PUll_CREATED'), 10),

    OneTimeTask(7, _('PROFILE_UPDATED'), 5),
    OneTimeTask(8, _('PROFILE_COMPLETE'), 20),

    DefaultTask(9, _('LOCATION_CREATED'), 3),
    OneTimeTask(10, _('FIRST_LOCATION_CREATED'), 5),

    DefaultTask(11, _('DEAL_CREATED'), 3),
    DefaultTask(12, _('BID_CREATED'), 1),
    # DefaultTask(13, _('BID_ANSWERED'), 1),
    # OneTimeTask(14, _('DEAL_FINISHED'), 10),

    DefaultTask(15, _('MARKET_CREATED'), 5),
    OneTimeTask(16, _('FIRST_MARKET_CREATED'), 10),

    # DefaultTask(17, _('CATEGORY_CREATED'), 2),  # After review! needs db change
    # OneTimeTask(18, _('FIRST_CATEGORY_CREATED'), 2),#dito

    OneTimeTask(19, _('FIRST_CHAT_MESSAGE'), 5),

    DefaultTask(20, _('USER_FEEDBACK_TAKEN'), 2),
    DefaultTask(21, _('PUSH_FEEDBACK_TAKEN'), 2),
    DefaultTask(22, _('USER_FEEDBACK_GIVEN'), 2),
    DefaultTask(23, _('PUSH_FEEDBACK_GIVEN'), 2),

    OneTimeTask(24, _('FIRST_CALC_DIRECT'), 3),
    # OneTimeTask(25, _('FIRST_CALC_TRIANGULAR'), 4),  # not yet implemented
    # OneTimeTask(26, _('FIRST_CALC_SPECULATIVE'), 5),  # not yet implemented
]

TASKS_CHOICES = [(obj.index, obj.title) for obj in TASKS]


def create_action(user, index_or_title):
    """ use this to create the action according to the task
    :param user: The user that fulfilled the task
    :param index_or_title: int(task.index) or str(unique_name-untranslated)
    :returns: True if it is created
    """
    action = False
    if isinstance(index_or_title, int):
        task = [task for task in TASKS if task.index == index_or_title]
    elif isinstance(index_or_title, str):
        task = [task for task in TASKS if task.title == _(index_or_title)]
    if task:
        task = task[0]
        action = Action.objects.create(user=user, task=task.index, exp=int(task.exp))
    return bool(action)


class Action(models.Model):
    """ Action is the fulfillment of a given task """
    user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('user'),
        )
    task = models.PositiveSmallIntegerField(
        default=0,
        choices=TASKS_CHOICES,
        verbose_name=_('task'),
        )
    exp = models.PositiveSmallIntegerField(
        default=0,
        verbose_name=_('experience'),
        )
    datetime = models.DateTimeField(
        auto_now_add=True,
        null=True,
        verbose_name=_('time'),
        )

    def get_task(self):
        """
        returns the task from the list according to the saved task
        """
        return [task for task in TASKS if task.index == self.task][0]

    def get_unique_name(self):
        """
        :returns: unique name of task
        """
        return self.get_task().unique_name

    def get_title(self):
        """
        :returns: task title str
        """
        return self.get_task().title

    def get_exp(self):
        """
        :returns: Exp()
        """
        return self.exp

    def save(self, *args, **kwargs):  # pylint: disable=signature-differs
        if not self.get_task().is_allowed(self.user):
            return False

        log_string = 'Action {}: user={} name={} exp={}'.format(
            'updated' if self.pk else 'created',
            str(self.user),
            str(self.get_title()),
            str(self.get_exp()),
            )
        LOGGER.info(log_string)

        msg = ngettext(
            'You earned %(exp)d experience point',
            'You earned %(exp)d experience points',
            self.get_exp(),
            ) % {'exp': int(self.get_exp())}
        msg += ': {}'.format(_(self.get_title()))
        api.info(self.user, mark_safe(msg))
        # LOGGER.info(log_string)
        super().save(*args, **kwargs)
        return True

    def __str__(self):
        return '{} {}({})'.format(
            str(self.user),
            str(self.get_title()),
            str(self.get_exp()),
            )

    class Meta:
        verbose_name = _('action')
        verbose_name_plural = _('actions')
