from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.db import models


def image_path(instance, filename):
    suffix = filename.split('.')[-1]
    return 'user/{}/avatar.{}'.format(instance.pk, suffix)


class UserConfig(models.Model):
    hint_step = models.PositiveSmallIntegerField(default=0)


class User(AbstractUser):

    config = models.OneToOneField(UserConfig, on_delete=models.CASCADE, null=True)
    image = models.ImageField(blank=True, upload_to=image_path)
    beta_user = models.BooleanField(default=False)
    description = models.TextField(blank=True)

    @property
    def locations(self):
        return self.location_set.all()

    @property
    def other_users(self):
        return self.__class__.objects.exclude(pk=self.pk)

    @property
    def pushs(self):
        return self.push_set.all()

    @property
    def pulls(self):
        return self.pull_set.all()

    @property
    def listings(self):
        """ returns list of listings (pushs and pulls) """
        return list(self.pushs) + list(self.pulls)

    @property
    def bids(self):
        return sorted(
            {*self.bids_sent.all(), *self.bids_received.all()},
            key=lambda x: x.datetime
            )

    @property
    def deals(self):
        deals = self.user1_deals.all().union(self.user2_deals.all())
        for deal in deals:
            deal.set_pov(self)
        return deals


@receiver(pre_save, sender=User)
def create_user_config(sender, instance, **kwargs):
    instance.config = UserConfig.objects.create()
