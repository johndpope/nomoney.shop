from django.utils.translation import gettext_lazy as _
from itertools import chain
from django.db import models


class CategoryStatus(models.IntegerChoices):
    UNPROVED = 0, _('unproved')
    PROVED = 10, _('proved')
    HIDDEN = 20, _('hidden')
    DELETED = 110, _('deleted')


class Category(models.Model):
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name=_('parent'),
        )
    title = models.CharField(
        max_length=50,
        verbose_name=_('title'),
        )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('description'),
        )
    status = models.PositiveSmallIntegerField(
        default=CategoryStatus.UNPROVED,
        choices=CategoryStatus.choices,
        verbose_name=_('status'),
        )

    @property
    def breadcrumbs(self):
        breadcrumbs = [self]
        obj = self
        while obj.parent:
            breadcrumbs = [obj.parent] + breadcrumbs
            obj = obj.parent
            print(breadcrumbs)
        return breadcrumbs

    @property
    def pushs(self):
        return self.push_set.all()

    @property
    def pulls(self):
        return self.pull_set.all()

    @property
    def count_pushs(self):
        return len(self.pushs)

    @property
    def count_pulls(self):
        return len(self.pushs)

    @property
    def listings(self):
        return list(chain(self.pushs, self.pulls))

    @property
    def path(self):
        obj = self
        title = self.title
        while obj.parent:
            title = obj.parent.title + '/' + title
            obj = obj.parent
        return title

    @classmethod
    def get_unproved(cls):
        return cls.objects.filter(status=CategoryStatus.UNPROVED)

    def __lt__(self, other):
        return len(self.listings) < len(other.listings)

    def __str__(self):
        if self.status == CategoryStatus.HIDDEN:
            return 'Hidden: ' + self.title
        return self.title

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        get_latest_by = ['pk']
