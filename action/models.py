""" models for the experience app

Experience is gained from doing actions

create actions from everywher like:
from action.models import tasks
action = tasks.add('PROFILE_VISITED', 1).action(user=request.user)

Pass request with action() to add a message to the request:
from django.utils.translation import gettext_lazy as _
msg = 'UNIQUE_STRING'
_(msg)
tasks.add(msg, 1).action(user=request.user, request=request)
"""
from enum import Enum
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib import messages
from django.utils.safestring import mark_safe
from config.settings import AUTH_USER_MODEL, LOGGER


__all__ = ['Exp', 'Action', 'tasks', 'messages']


class Exp(int):
    """ Exp is the number of gained experience points """

    @property
    def level(self):
        """
        :returns: level of this exp value
        """
        return Level.by_exp(self)


class Level(Enum):
    """ these are the exp values to reach level
    CONST = Exp(0), _('const')
    """
    ROOKIE = Exp(0), _('rookie')
    BEGINNER = Exp(10), _('beginner')
    ARRIVED = Exp(50), _('arrived')
    MIDDLE = Exp(100), _('middle')
    ADVANCED = Exp(250), _('advanced')
    SEMIPRO = Exp(1000), _('semipro')
    PROFI = Exp(5000), _('profi')
    LEGEND = Exp(10000), _('legend')
    IMMORTAL = Exp(100000), _('immortal')

    @classmethod
    def levels(cls):
        """
        :returns: all levels sorted
        """
        return sorted(cls, key=lambda x: x.value[0])

    @classmethod
    def stages(cls):
        """
        :returns: list of Exp values of the levels
        """
        return [level.value[0] for level in cls.levels()]

    @classmethod
    def by_exp(cls, exp):
        """ select level by number
        :param exp:
        :returns: Level
        """
        seq = [level for level in cls.levels() if level.value[0] < Exp(exp)]
        if seq:
            return max(seq)
        return cls.ROOKIE

    def __lt__(self, other):
        # pylint: disable=unsubscriptable-object
        return self.value[0] < other.value[0]

    def __str__(self):
        # pylint: disable=unsubscriptable-object
        return str(_(self.value[1]))


class _Task:
    """ Possible fulfillments of an action
    :param title: str with title
    """
    def __init__(self, title, exp, exp_needed=0):
        self.name = title[:50]
        self.exp = Exp(exp)
        self.exp_needed = exp_needed

    def is_allowed(self, user):
        """ Is it allowed to fulfill this task?
        :param exp: Exp() to check
        :returns: bool(True) if exp is bigger than needed
        """
        return user.exp >= self.exp_needed

    def action(self, user, request=None):
        """ create action from this task
        :param user: User that fulfilled the task
        :param request: if passed, it creates a message for the frontend
        """
        if self.is_allowed(user):
            Action.objects.create(
                user=user,
                name=self.name,
                exp=self.exp
                )
        if request:
            msg = '{} {}{}:<br />"{}"'.format(
                str(_('you earned')).title(),
                str(self.exp),
                str(_('exp')),
                str(_(self.name)),
                )
            messages.add_message(
                request,
                messages.INFO,
                mark_safe(msg)
                )

    def __str__(self):
        return str(_(self.name))


class _Tasks(dict):
    """ enum constants can be enhanced by per-app tasks
    do not instantiate
    CONST = Task(_('CONST'), Exp(), exp_needed=0), _('CONST')
    """
    def get(self, unique_name):
        return self[unique_name]

    def add(self, unique_name, exp, exp_needed=0):
        """ use this to create tasks from outside """
        unique_name = unique_name.upper()
        self[unique_name] = _Task(unique_name, Exp(exp), exp_needed=exp_needed)
        return self[unique_name]

    def __str__(self):
        tasks_str = [str(task) for task in self.values()]
        return 'Tasks: {}'.format(','.join(tasks_str))


tasks = _Tasks()


class Action(models.Model):
    """ Action is the fulfillment of a given task """
    user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('user'),
        )
    name = models.CharField(
        max_length=50,
        verbose_name=_('title'),
        )
    exp = models.PositiveIntegerField(
        default=Level.ROOKIE,
        verbose_name=_('experience'),
        )
    seen_by = models.ManyToManyField(
        AUTH_USER_MODEL,
        related_name='seen_action',
        verbose_name=_('seen_by'),
        )

    def get_exp(self):
        """
        :returns: Exp()
        """
        return Exp(self.exp)

    def add_seen_by(self, user):
        """ adds a user that has seen this action
        :param user: user object
        """
        self.seen_by.add(user)
        self.save()

    def save(self, *args, **kwargs):  # pylint: disable=signature-differs
        log_string = 'Action {}: user={} name={} exp={}'.format(
            'updated' if self.pk else 'created',
            str(self.user),
            str(self.name),
            str(self.exp),
            )
        LOGGER.info(log_string)
        super().save(*args, **kwargs)

    def __str__(self):
        return '{} {}({})'.format(
            str(self.user),
            str(_(self.name)),
            str(self.get_exp()),
            )

    class Meta:
        verbose_name = _('action')
        verbose_name_plural = _('actions')
