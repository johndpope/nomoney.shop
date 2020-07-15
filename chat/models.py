from django.utils.translation import gettext_lazy as _
from django.db import models
from config.settings import AUTH_USER_MODEL


class ChatType(models.IntegerChoices):
    DEFAULT = 0, _('default')
    USER = 10, _('user')
    MARKET = 20, _('market')
    LOBBY = 100, _('lobby')

    @classmethod
    def by_number(cls, number):
        return cls(number)


class ChatMessage(models.Model):
    chat = models.ForeignKey(
        'chat.Chat',
        on_delete=models.CASCADE,
        verbose_name=_('chat'),
        )
    creator = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('creator'),
        )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('created'),
        )
    text = models.TextField(
        verbose_name=_('text'),
        )

    @property
    def previous(self):
        message_list = list(ChatMessage.objects.filter(chat=self.chat))
        index = message_list.index(self)
        if index:
            return message_list[index-1]

    class Meta:
        ordering = ['-pk']
        verbose_name = _('message')
        verbose_name_plural = _('message')


class Chat(models.Model):
    """
    Chats are used by multiple models in different ways:
    User-Chat: Is created by the combination of users (Chat.by_users)
    Market-Chat: Is created within Market.save
    lobby-chat: Is a single object fetched and created by Chat.get_lobby
    """
    users = models.ManyToManyField(
        AUTH_USER_MODEL,
        verbose_name=_('text'),
        )
    type = models.PositiveSmallIntegerField(
        default=ChatType.DEFAULT,
        choices=ChatType.choices,
        verbose_name=_('type'),
        )
    market = models.OneToOneField(
        'market.Market',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name=_('market'),
        )

    @property
    def type_str(self):
        return ChatType.by_number(self.type).label

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
    def by_users(cls, *users, create=False):
        chats = cls.objects.filter(type=ChatType.USER)
        for chat in chats:
            if set(chat.users.all()) == set(users):
                return chat

        if create:
            chat = cls.objects.create(type=ChatType.USER)
            for user in users:
                chat.users.add(user)
            chat.save()
            return chat

        return None

    def __str__(self):
        if self.type == ChatType.LOBBY:
            return 'Lobby'
        user_str = ', '.join((str(user) for user in self.get_users()))
        return 'Chat [{}]: {}'.format(self.type_str, user_str)

    class Meta:
        verbose_name = _('chat')
        verbose_name_plural = _('chats')
