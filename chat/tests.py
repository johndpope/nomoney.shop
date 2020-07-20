""" tests for the chat module """
from tests_abc import TestCase
from .models import Chat, ChatType, ChatMessage
from user.models import User


class ChatTestCase(TestCase):
    """ tests for the chat module """

    def setUp(self):
        super().setUp()
        self.lobby = Chat.get_lobby()
        self.all_users = User.get_users()

    def test_views(self):
        self.anon.get302('chat_list')
        self.user.get200('chat_list')
        self.anon.get302('chat_detail', url_args=self.lobby.pk)
        self.user.get200('chat_detail', url_args=self.lobby.pk)
        self.anon.get302('chat_user_detail', url_args=self.demo.pk)
        self.user.get200('chat_user_detail', url_args=self.demo.pk)
        
        self.anon.get302('chat_user_detail', url_args=self.demo.pk)
        self.user.get200('chat_user_detail', url_args=self.demo.pk)
        
        self.user.post302('chat_new_message', url_args=self.lobby.pk, data={'text': 'bla'})

    def test_chat_models_lobby(self):
        """ test lobby chat models """
        # Lobby
        lobby = self.lobby
        self.assertEqual(Chat.get_lobby(), Chat.get_lobby())
        self.assertEqual(lobby.type, ChatType.LOBBY)
        self.assertEqual(lobby.type, ChatType.by_number(lobby.type))
        self.assertEqual(str(lobby), 'Lobby')
        #self.assertEqual(set(lobby.get_users()), set(User.get_users()))

    def test_chatmessage_models_lobby(self):
        lobby = self.lobby
        self.assertFalse(lobby.messages)
        msg1 = lobby.add_message(self.demo, 'test0')
        self.assertEqual(str(msg1), msg1.text)
        self.assertTrue(lobby.messages)
        self.assertIsNone(lobby.messages[0].previous)
        msg2 = ChatMessage.objects.create(chat=lobby, creator=self.demo1, text='test1')
        self.assertEqual(msg1.next, msg2)
        self.assertEqual(msg2.previous, msg1)
        self.assertIsNone(msg1.previous)
        self.assertIsNone(msg2.next)

        # pylint: disable=no-member
        self.assertEqual(self.lobby.type_str, ChatType.LOBBY.label)

    def test_chatmessage_models_market(self):
        chat = self.market.chat
        self.assertIsInstance(chat, Chat)
        msg = chat.add_message(self.demo, 'test0')
        self.assertEqual(set(msg.unseen_by.all()), set(chat.get_users()))
        self.assertIn(self.demo, set(msg.unseen_by.all()))
        msg.set_seen_by(self.demo)
        self.assertNotIn(self.demo, set(msg.unseen_by.all()))

        msg2 = chat.add_message(self.demo, 'test2')
        self.assertIn(self.demo1, set(msg.unseen_by.all()))
        self.assertIn(self.demo1, set(msg2.unseen_by.all()))
        chat.all_messages_seen_by(self.demo1)
        self.assertNotIn(self.demo1, set(msg.unseen_by.all()))
        self.assertNotIn(self.demo1, set(msg2.unseen_by.all()))

        self.assertIsNone(Chat.by_users(self.demo, self.demo1))
        chat = Chat.by_users(self.demo, self.demo1, create=True)
        self.assertIsInstance(chat, Chat)
        self.assertEqual(chat, Chat.by_users(self.demo, self.demo1))
        self.assertIsInstance(str(chat), str)
