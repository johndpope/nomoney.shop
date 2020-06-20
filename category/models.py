from itertools import chain
from django.db import models


class Category(models.Model):
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    hidden = models.BooleanField(default=False)

    @property
    def pushs(self):
        return self.push_set.all()

    @property
    def pulls(self):
        pass
        return self.pull_set.all()

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

    def count_actions(self):
        return 1 #len(self.listings)

    def __lt__(self, other):
        return self.count_actions() < other.count_actions()

    def __str__(self):
        return self.path

    class Meta:
        verbose_name_plural = "Categories"
