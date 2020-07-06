from uuid import uuid4
from itertools import chain
from django.db import models
from config.settings import AUTH_USER_MODEL
from chat.models import Chat
from statistics import mean


def image_path(instance, _):
    return 'listing/{}/{}'.format(instance.type, uuid4())


class ListingStatus(models.IntegerChoices):
    CREATED = 0, 'created'
    DELETED = 110, 'deleted'


class Unit(models.Model):
    title = models.CharField(max_length=20)
    short = models.CharField(max_length=5)

    def __str__(self):
        return self.title


class ListingBase(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, )
    title = models.CharField(max_length=50)
    category = models.ForeignKey('category.Category', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, upload_to=image_path)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    location = models.ForeignKey(
        'location.Location', on_delete=models.CASCADE, blank=True, null=True
        )
    test = models.BooleanField(default=False)
    status = models.PositiveSmallIntegerField(
        default=ListingStatus.CREATED, choices=ListingStatus.choices
        )
    type = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._actions = {0: set(), 1: set(), 2: set(), 3: set()}

    @property
    def opposite_class(self):
        return {'push': Pull, 'pull': Push}.get(self.type)

    def get_chat_with_partner(self, partner):
        return Chat.by_users(self.user, partner, create=True)

    def get_matches(self):
        cls = self.opposite_class
        return cls.objects.filter(category=self.category
                                  ).exclude(user=self.user)

    @staticmethod
    def get_all():
        return list(chain(Push.objects.all(), Pull.objects.all()))

    # pylint: disable=signature-differs, unused-argument
    def delete(self, *args, **kwargs):
        self.status = ListingStatus.DELETED
        self.save()

    def __eq__(self, other):
        try:
            return self.category == other.category
        except AttributeError as e:
            print(e)

    def __str__(self):
        # pylint: disable=no-member
        return '{} {} {}'.format(self.user.username, self.type, self.title)

    class Meta:
        abstract = True


class Push(ListingBase):
    type = 'push'

    @property
    def score(self):
        scores = []
        for feedback in self.pushfeedback_set.all():
            if feedback.score:
                scores.append(feedback.score)
        if scores:
            return mean(scores)

    @property
    def feedbacks(self):
        return self.pushfeedback_set.all()


class Pull(ListingBase):
    type = 'pull'
