from enum import Enum
from django.db import models
from django.utils.translation import gettext_lazy as _


class Exp(int):
    """ Exp is the number of gained experience points """

    @property
    def level(self):
        """
        :returns: level of this exp value
        """
        return Level.by_exp(self)


class Level(models.IntegerChoices):
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

    def get_value(self):
        return self.value

    def get_name(self):
        return self.name

    def get_label(self):
        return self.label

    @classmethod
    def min_level(cls):
        """
        :returns: minimum existing level
        """
        return cls.levels()[0]

    @classmethod
    def max_level(cls):
        """
        :returns: maximum existing level
        """
        return cls.levels()[-1]

    @classmethod
    def levels(cls):
        """
        :returns: all levels sorted
        """
        return sorted(cls, key=lambda x: x.value)

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
        seq = [level for level in cls.levels() if level.get_value() < Exp(exp)]
        if seq:
            return max(seq)
        return cls.ROOKIE

    def __lt__(self, other):
        # pylint: disable=unsubscriptable-object
        return self.value[0] < other.value[0]

    def __str__(self):
        # pylint: disable=unsubscriptable-object
        return str(_(self.get_name()))
