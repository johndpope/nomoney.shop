""" models of the category module """
from itertools import chain
from django.utils.translation import gettext_lazy as _
from django.db import models
from config.settings.base import LOGGER


class CategoryStatus(models.IntegerChoices):
    """ Status of the Category object
    UNPROVED - New created category, not reviewed by admin
    PROVED - Category was proved by the admin
    HIDDEN - Category is hidden but active
    DELETED - Category is deleted (inactive)
    """
    UNPROVED = 0, _('unproved')
    PROVED = 10, _('proved')
    HIDDEN = 20, _('hidden')
    DELETED = 110, _('deleted')


class Category(models.Model):
    """ Categories are used for comparing services and goods """
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
        """ Path of this category with its parents for creating breadcrumbs
        :returns: list of parents of this category
        """
        breadcrumbs = [self]
        obj = self
        while obj.parent:
            breadcrumbs = [obj.parent] + breadcrumbs
            obj = obj.parent
        return breadcrumbs

    @property
    def pushs(self):
        """ pushs of this category
        :returns: QuerySet of push objects
        """
        return self.push_set.all()

    @property
    def pulls(self):
        """ pulls of this category
        :returns: QuerySet of pull objects
        """
        return self.pull_set.all()

    @property
    def listings(self):
        """ All listings of this category (pushs and pulls)
        :returns: list of push+pulls
        """
        return list(chain(self.pushs, self.pulls))

    @property
    def path(self):
        """ Category name as path (DEPRECATED)
        :returns: str
        """
        obj = self
        title = self.title
        while obj.parent:
            title = obj.parent.title + '/' + title
            obj = obj.parent
        return title

    @classmethod
    def get_unproved(cls):
        """ all unproved categories
        :returns: QuerySet of unproved categories
        """
        return cls.objects.filter(status=CategoryStatus.UNPROVED)

    @classmethod
    def get_hidden(cls):
        """ all hidden categories
        :returns: QuerySet of hidden categories
        """
        return cls.objects.filter(status=CategoryStatus.HIDDEN)

    @classmethod
    def get_deleted(cls):
        """ all deleted categories
        :returns: QuerySet of deleted categories
        """
        return cls.objects.filter(status=CategoryStatus.DELETED)

    def save(self, *args, **kwargs):  # pylint: disable=signature-differs
        log_string = 'Category {}: path={} status={}'.format(
            'updated' if self.pk else 'created',
            '.'.join((str(breadcrumb) for breadcrumb in self.breadcrumbs)),
            str(self.status),
            )
        LOGGER.info(log_string)
        super().save(*args, **kwargs)

    def __lt__(self, other):
        return len(self.listings) < len(other.listings)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        get_latest_by = ['pk']
