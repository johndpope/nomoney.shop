from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save
from config.settings import AUTH_USER_MODEL
from chat.models import Chat


class Guild(models.Model):
    users = models.ManyToManyField(AUTH_USER_MODEL)
    chat = models.OneToOneField('chat.Chat', on_delete=models.CASCADE)
    title = models.CharField(max_length=20)

############
@receiver(pre_save, sender=Guild)
def create_chat(sender, instance, created, **kwargs):
    import pdb; pdb.set_trace()  # <---------
    if created:
        Chat.objects.create(user=instance)