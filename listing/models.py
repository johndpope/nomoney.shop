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
        return Listing.objects.filter(category=self, type='push')

    @property
    def pulls(self):
        return Listing.objects.filter(category=self, type='pull')

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
    type = models.CharField(max_length=4, choices=TYPES)
    title = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    count = models.DecimalField(
        decimal_places=2,
        max_digits=12,
        validators=[MinValueValidator(Decimal('0.01'))]
        )
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    reviews = models.ForeignKey(Review, null=True, blank=True, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._actions = {0: set(), 1: set(), 2: set(), 3: set()}

    def actions(self):
        """ An action is a possible dealable listing.
        It must be from another user and another type.
        """
        actions = {0: set(), 1: set(), 2: set(), 3: set()}
        if not self._actions or True:  # disable cache for testing
            objects = __class__.objects.filter(category=self.category)
            objects = objects.exclude(type=self.type).exclude(user=self.user)
            for action in objects:
                if action not in self.user.listings.exclude(type=action.type):
                    actions[1].add(action)
                if 
            import pdb; pdb.set_trace()  # <---------
        return self._actions

    def level1(self):
        """ returns set of level 1 dealsets """
        import pdb; pdb.set_trace()  # <---------
        return self.actions()

    def level2(self):
        actions = set()
        for action in self.actions():
            possible_actions = action.user.listings.exclude(type=action.type)
            if action in possible_actions:
                actions.add(action)
        return actions

#    def __hash__(self):
#        return hash(self.pk)

    def __eq__(self, other):
        return self.category == other.category

    def __hash__(self):  # TODO: equaling items have different hashs?
        return hash(self.pk)

    def __str__(self):
        return self.type + ': ' + self.title
