from django.db import models
from config.settings import AUTH_USER_MODEL


class Deal(models.Model):
    user1 = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='deals_user1')
    user2 = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='deals_user2')
    accepted = models.BooleanField(default=False)

    @property
    def users(self):
        return self.user1, self.user2
