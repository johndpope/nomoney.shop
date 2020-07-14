from itertools import chain
from django.db import models


class CategoryStatus(models.IntegerChoices):
    UNPROVED = 0, 'unproved'
    PROVED = 10, 'proved'
    HIDDEN = 20, 'hidden'
    DELETED = 110, 'deleted'


class Category(models.Model):
    parent = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.CASCADE
        )
    title = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    status = models.PositiveSmallIntegerField(
        default=CategoryStatus.UNPROVED,
        choices=CategoryStatus.choices,
        )

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
        return self.path

    class Meta:
        verbose_name_plural = "Categories"
        get_latest_by = ['pk']
