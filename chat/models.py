from django.db import models
from config.settings import AUTH_USER_MODEL


class ChatType(models.IntegerChoices):
    DEFAULT = 0, 'default'
    USER = 10, 'user'
    MARKET = 20, 'market'
    LOCATION = 30, 'location'
    DEAL = 40, 'deal'
    LOBBY = 100, 'lobby'


class ChatMessage(models.Model):
    chat = models.ForeignKey('chat.Chat', on_delete=models.CASCADE, )
    creator = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, )
    created = models.DateTimeField(auto_now_add=True)
    text = models.TextField()

    @property
    def previous(self):
        message_list = list(ChatMessage.objects.filter(chat=self.chat))
        index = message_list.index(self)
        if index:
            return message_list[index-1]

    class Meta:
        ordering = ['-pk']


class Chat(models.Model):
    users = models.ManyToManyField(AUTH_USER_MODEL)
    type = models.PositiveSmallIntegerField(
        default=ChatType.DEFAULT,
        choices=ChatType.choices,
        )

    @classmethod
    def get_lobby(cls):
        try:
            return cls.objects.get(type=ChatType.LOBBY)
        except Chat.DoesNotExist:
            return cls.objects.create(type=ChatType.LOBBY)

    @property
    def title(self):
        if self.users.all():
            return ', '.join((str(user) for user in self.users.all()))
        return 'Chat: {}'.format(self.pk)

    @property
    def messages(self):
        return self.chatmessage_set.all()

    @classmethod
    def by_users(cls, *user_list, create=False, virtual=False):
        chats = cls.objects.all()
        for chat in chats:
            if set(chat.users.all()) == set(user_list):
                return chat

        if create:
            chat = cls.objects.create()
            for user in user_list:
                chat.users.add(user)
            chat.save()
            return chat

        return None

    def save(self, *args, **kwargs):
        if self.type == ChatType.LOBBY:
            return self.get_lobby()
        return models.Model.save(self, *args, **kwargs)

    def __str__(self):
        return self.title
