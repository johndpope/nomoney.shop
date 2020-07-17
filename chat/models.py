""" models for chat module """
from django.utils.translation import gettext_lazy as _
from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save
from django.db import models
from config.settings import AUTH_USER_MODEL


class ChatType(models.IntegerChoices):
    """ Type of the Chat
    DEFAULT - No chat should become that
    USER - Chat with user constellation as selector
    MARKET - Chat that is created by market (dynamic user constellation)
    LOBBY - One single chat that is used by all (no/dynamic user constellation)
    """
    DEFAULT = 0, _('default')
    USER = 10, _('user')
    MARKET = 20, _('market')
    LOBBY = 100, _('lobby')

    @classmethod
    def by_number(cls, number):
        """ select chat type by number
        :param number: integer of the chat type to select
        :returns: ChatType.X
        """
        return cls(number)


class ChatMessage(models.Model):
    """
    creates list of all users that should see this message.
    when user has seen the message, he will be removed from that list.
    """
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

    unseen_by = models.ManyToManyField(
        AUTH_USER_MODEL,
        related_name='unseen_messages',
        verbose_name=_('unseen_by'),
        )

    @property
    def previous(self):
        """ get previous chat message
        :returns: ChatMessage or None
        """
        message_list = list(ChatMessage.objects.filter(chat=self.chat))
        index = message_list.index(self)
        if index:
            return message_list[index-1]
        return None

    def set_seen_by(self, user):
        """ set message seen by
        :param user: user object that accessed this message
        """
        self.unseen_by.remove(user)
        self.save()

    def save(self, *args, **kwargs):  # pylint: disable=signature-differs
        super().save(*args, **kwargs)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['-pk']
        verbose_name = _('message')
        verbose_name_plural = _('message')


@receiver(post_save, sender=ChatMessage)
# pylint: disable=unused-argument
def create_user_config(sender, instance, created, **kwargs):
    """ add all users that should see the chat into unseen_by """
    if created:
        for user in instance.chat.get_users():
            instance.unseen_by.add(user)
        instance.save()


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
        """ get type as string instead of integer
        :returns: str
        """
        return ChatType.by_number(self.type).label

    @property
    def messages(self):
        """ get messages of this chat
        :returns: QuerySet of ChatMessage objects
        """
        return self.chatmessage_set.all()

    def all_messages_seen_by(self, user):
        """ mark all messages as seen by user
        :param user: User object that has seen all chat messages
        """
        for message in self.messages:
            if user in message.unseen_by.all():
                message.set_seen_by(user)

    def get_users(self):
        """ get users of this chat
        :returns: QuerySet of Users
        """
        if self.type == ChatType.MARKET:
            return self.market.users.all()
        return self.users.all()

    @classmethod
    def get_lobby(cls):
        """ get singleton lobby chat
        :returns: Chat object
        """
        try:
            return cls.objects.get(type=ChatType.LOBBY)
        except Chat.DoesNotExist:
            return cls.objects.create(type=ChatType.LOBBY)

    @classmethod
    def _create_user_object(cls, *users):
        chat = cls.objects.create(type=ChatType.USER)
        for user in users:
            chat.users.add(user)
        chat.save()
        return chat

    @classmethod
    def by_users(cls, *users, create=False):
        """ get chat by user constellation
        :returns: Chat or None
        """
        chats = cls.objects.filter(type=ChatType.USER)
        for chat in chats:
            if set(chat.users.all()) == set(users):
                return chat

        if create:
            chat = cls._create_user_object(*users)
            return chat
        return None

    def __str__(self):
        if self.type == ChatType.LOBBY:
            return 'Lobby'
        user_str = ', '.join((str(user) for user in self.get_users()))
        return 'Chat [{}]: {}'.format(self.type_str, user_str)

    class Meta:
        ordering = ['-type']
        verbose_name = _('chat')
        verbose_name_plural = _('chats')
