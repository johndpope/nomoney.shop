""" chat consumer created during channels tutorial """
# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.db import database_sync_to_async


class ChatConsumer(WebsocketConsumer):
    """ chat consumer created during channels tutorial """
    room_name = None
    room_group_name = None

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    # pylint: disable=arguments-differ, unused-argument
    def disconnect(self, close_code):
        """ Leave room group """
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        """ Receive message from WebSocket """
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    @database_sync_to_async
    def save_message(self):
        """ FUTURE - create new message object when received """

    def chat_message(self, event):
        """ Receive message from room group """
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))
