from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator
from config.settings import AUTH_USER_MODEL

TYPES = (
    ('push', 'Biete'),
    ('pull', 'Suche'),
    )

class Category(models.Model):
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)

    @property
    def pushs(self):
        return Push.objects.filter(category=self)

    @property
    def pulls(self):
        return Pull.objects.filter(category=self)

    @property
    def path(self):
        obj = self
        title = self.title
        while obj.parent:
            title = obj.parent.title + '/' + title
            obj = obj.parent
        return title

    def __lt__(self, other):
        return str(self) < str(other)

    def __str__(self):
        return self.path

    class Meta:
        verbose_name_plural = "Categories"


class Review(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    score = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.title


class Unit(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Listing(models.Model):
    user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        )
    title = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    quantity = models.DecimalField(
        decimal_places=2,
        max_digits=12,
        validators=[MinValueValidator(Decimal('0.01'))]
        )
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    type = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._actions = {0: set(), 1: set(), 2: set(), 3: set()}

    def matches(self):
        """ Returns same category objects of other users with other type """
        import pdb; pdb.set_trace()  # <---------
        #=======================================================================
        # return __class__.objects.filter(category=self.category
        #                                 ).exclude(type=self.type
        #                                           ).exclude(user=self.user)
        #=======================================================================

    def opposite_type(self):
        return {'push': 'pull', 'pull': 'push'}.get(self.type)

    def __eq__(self, other):
        return self.category == other.category  # and self.type == other.type

    def __str__(self):
        return '{} {} {}'.format(self.user.username, self.type, self.title)

    class Meta:
        abstract = True

class Push(Listing):
    type = 'push'

class Pull(Listing):
    type = 'pull'
