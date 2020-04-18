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

#    def __hash__(self):
#        return hash(self.pk)

    #===========================================================================
    # def level1(self):
    #     """ returns matches with only one side to deal """
    #     result = []
    #     users = {match.user for match in self.matches()}
    #     level = 0
    #     for user in users:
    #         for push in self.user.pushs:
    #             import pdb; pdb.set_trace()  # <---------
    #             if push in user.pulls:
    #                 level += 1
    #         for pull in self.user.pulls:
    #             if pull in user.pushs:
    #                 level +=1
    #===========================================================================
        #=======================================================================
        # for user in users:
        #     self.user.matches(user)
        #     for listing in user.listings:
        #         listing_users = {bla.user for bla in listing.matches()}
        #         if self.user in listing_users:
        #             print('level2')
        #         else:
        #             print('level1')
        #     
        # for match in self.matches():
        #     if self.user in [submatch.user for submatch in match.matches()]:
        #         result.append(match)
        #         
        #=======================================================================

    def matches(self):
        """ Returns same category objects of other users with other type """
        return __class__.objects.filter(category=self.category
                                        ).exclude(type=self.type
                                                  ).exclude(user=self.user)

    #===========================================================================
    # def mediator(self):
    #     # 
    #     result = __class__.objects.filter()
    #===========================================================================

    def __eq__(self, other):
        return self.category == other.category  # and self.type == other.type

    def __hash__(self):  # TODO: equaling items have different hashs?
        return hash(self.category)

    def __str__(self):
        return self.type + ': ' + self.title
