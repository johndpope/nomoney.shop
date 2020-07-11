from django.db import models
from config.settings import AUTH_USER_MODEL


class ChatType(models.IntegerChoices):
    DEFAULT = 0, 'default'
    USER = 10, 'user'
    MARKET = 20, 'market'
    LOBBY = 100, 'lobby'

    @classmethod
    def by_number(cls, number):
        return cls(number)


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
    """
    Chats are used by multiple models in different ways:
    User-Chat: Is created by the combination of users (Chat.by_users)
    Market-Chat: Is created within Market.save
    lobby-chat: Is a single object fetched and created by Chat.get_lobby
    """
    users = models.ManyToManyField(AUTH_USER_MODEL)
    type = models.PositiveSmallIntegerField(
        default=ChatType.DEFAULT,
        choices=ChatType.choices,
        )
    market = models.OneToOneField('market.Market', null=True, blank=True,
                                  on_delete=models.CASCADE)

    @property
    def type_str(self):
        return ChatType.by_number(self.type).label

    @property
    def title(self):
        if self.users.all():
            return ', '.join((str(user) for user in self.users.all()))
        return 'Chat: {}'.format(self.pk)

    @property
    def messages(self):
        return self.chatmessage_set.all()

    def get_users(self):
        if self.type == ChatType.MARKET:
            return self.market.users.all()
        return self.users.all()

    @classmethod
    def get_lobby(cls):
        try:
            return cls.objects.get(type=ChatType.LOBBY)
        except Chat.DoesNotExist:
            return cls.objects.create(type=ChatType.LOBBY)

    @classmethod
    def by_users(cls, *user_list, create=False, virtual=False):
        chats = cls.objects.filter(type=ChatType.USER)
        for chat in chats:
            if set(chat.users.all()) == set(user_list):
                return chat

        if create:
            chat = cls.objects.create(type=ChatType.USER)
            for user in user_list:
                chat.users.add(user)
            chat.save()
            return chat

        return None

    def __str__(self):
        return 'Chat [{}]:'.format(self.type_str)
