from django.db import models


class Action(models.Model):
    comment = models.TextField()

    class Meta:
        abstract = True


class Push(Action):
    pass


class Pull(Action):
    pass