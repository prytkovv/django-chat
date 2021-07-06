from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json

from django.contrib.auth.models import User
from .models import Message, Room


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive messgae from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': self.scope['user'].username,
            }
        )

    #Receive message from room group
    def chat_message(self, event):
        username = event['username']
        message = event['message']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'username': username,
        }))
        self.save_message(username, message)

    def get_user_by_username(self, username):
        # check this
        return User.objects.get(username=username)

    def save_message(self, username, message):
        message = Message.objects.create(
            user=self.get_user_by_username(username), text=message)
        return message
