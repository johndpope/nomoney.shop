from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .exp import Exp, Level

__all__ = ['DefaultTask', 'DailyTask', 'OneTimeTask']


class DefaultTask:
    """ Possible fulfillments of an action
    :param title: str with title
    :param min_level: minimum level for this task (defaults to lowest)
    :param max_level: maximum level for this task (defaults to None)
    """
    type = _('default')
    order = 1

    def __init__(self, index, title, exp, *args):
        self.index = index
        self.title = title
        self.exp = exp
        self.exp = Exp(exp)
        self.min_level = args[0] if args else Level.min_level()
        self.max_level = args[1] if len(args) >= 2 else None

    def _is_allowed(self, user):
        """ Is it allowed to fulfill this task?
        :param exp: Exp() to check
        :returns: bool(True) if exp is bigger than needed
        """
        if self.max_level:
            return self.min_level.exp <= user.exp < self.max_level.exp
        return self.min_level.exp <= user.exp

    def is_allowed(self, user):  # pylint: disable=no-self-use, unused-argument
        """ overwrite this if needed
        :returns: True
        """
        return True

    def __lt__(self, other):
        if self.order < other.order:
            return True
        elif self.order > other.order:
            return False
        else:
            return self.title < other.title

    def __str__(self):
        return str(_(self.title))


class DailyTask(DefaultTask):  # pylint: disable=too-few-public-methods
    """ This objects can be actioned once per day """
    type = _('daily')
    order = 2

    def is_allowed(self, user):
        today_actions = user.actions.filter(
            task=self.index,
            datetime__gte=timezone.now().replace(hour=0, minute=0, second=0)
            )
        return not today_actions  # True if not today_actions


class OneTimeTask(DefaultTask):  # pylint: disable=too-few-public-methods
    """ This task can only be actioned once per user """
    type = _('onetime')
    order = 3

    def is_allowed(self, user):
        return self.index not in user.actions.values_list('task', flat=True)
