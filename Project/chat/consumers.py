import json

from django.contrib.auth import get_user_model
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from .models import Message


User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_name = None
        self.room_group_name = None

    async def fetch_messages(self, data):
        messages = Message.last_20_messages()
        content = {
            'command': 'messages',
            'messages': await self.messages_to_json(messages),
        }
        await self.send_message(content)

    async def new_message(self, data):
        author = data['from']
        content = data['message']
        message = await self.save_message_to_database(author, content)
        content = {
            'command': 'new_message',
            'message': await self.message_to_json(message)
        }
        await self.send_chat_messages(content)

    @database_sync_to_async
    def save_message_to_database(self, author, content):
        author_user = User.objects.filter(username=author).first()
        message = Message.objects.create(
            author=author_user,
            content=content)
        return message

    async def messages_to_json(self, messages):
        # return [await self.message_to_json(message) for message in messages]
        return ['hello', 'hi']

    async def message_to_json(self, message):
        return {
            'author': message.author.username,
            'content': message.content,
            'timestamp': str(message.timestamp),
        }

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message,
    }

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        await self.commands[data['command']](self, data)

    async def send_chat_messages(self, message):
        await self.channel_layer.group_send(self.room_group_name, {'type': 'chat.message', 'message': message})

    async def send_message(self, message):
        await self.send(text_data=json.dumps(message))

    async def chat_message(self, event):
        message = event['message']
        print(message)

        await self.send(text_data=json.dumps(message))
