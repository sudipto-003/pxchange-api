from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import Chat, Message
from channels.db import database_sync_to_async
from .serializers import MessageSerializer

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        user2 = self.scope['url_route']['kwargs']['recipent']
        self.user1 = self.scope['user']
        self.chat = await self.get_chat(self.user1.username, user2)
        self.chat_group_name = f'chat_{self.chat.id}'

        await self.channel_layer.group_add(
            self.chat_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self):
        await self.channel_layer.group_discard(
            self.chat_group_name,
            self.channel_name
        )

    async def receive(self, data):
        json_data = json.loads(data)
        message = json_data['message']

        message_instance = await message_save(message)
        serialized_message = MessageSerializer(message_instance)

        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                'type': 'send_text_message',
                'message': serialized_message.data
            }
        )

    async def send_text_message(self, event):
        message_data = event['message']

        await self.send(data=message_data)

    @database_sync_to_async
    def get_chat(self, username1, username2):
        chat_instance, _ = Chat.objects.get_or_create(username1, username2)

        return chat_instance

    @database_sync_to_async
    def message_save(self, message):
        return Message.objects.create(sender=self.user1, text=message, chatbox=self.chat)