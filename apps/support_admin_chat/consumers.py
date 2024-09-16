import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatRoom, ChatMessage


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope["user"].id

        # Определяем группу в зависимости от роли (админ или пользователь)
        if self.scope["user"].is_staff:
            self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
            self.room_group_name = f'chat_{self.room_id}'
        else:
            self.room_group_name = f'chat_{self.user_id}'
            self.room_id = self.user_id

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        # Если это администратор, помечаем все сообщения в этой комнате как прочитанные
        if self.scope["user"].is_staff:
            await self.mark_messages_as_read(self.room_id)

        # Отправляем предыдущие сообщения (загружаем историю)
        # await self.send_previous_messages(self.room_id)

    async def disconnect(self, close_code):
        # Отключение от группы
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        print(text_data)
        text_data_json = json.loads(text_data)

        # Если это уведомление об открытии чата
        if text_data_json.get('type') == 'chat_opened':
            await self.mark_messages_as_read(self.room_id)

        # Получаем сообщение из данных
        message = text_data_json.get('message')

        if message:
            # Сохраняем сообщение
            print(message + " " + str(self.user_id))
            await self.save_message(self.user_id, message)

            # Отправляем сообщение всем участникам чата
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender_id': self.user_id,
                    'sender_username': self.scope['user'].phone_number
                }
            )

    async def chat_message(self, event):
        message = event['message']
        sender_id = event['sender_id']
        sender_username = event['sender_username']

        # Отправляем сообщение клиенту
        await self.send(text_data=json.dumps({
            'message': message,
            'sender_id': sender_id,
            'sender_username': sender_username,
        }))

        # Если чат открыт администратором, отмечаем входящее сообщение как прочитанное
        if self.scope["user"].is_staff:
            await self.mark_messages_as_read(self.room_id)

    @database_sync_to_async
    def save_message(self, user_id, message):
        # Определяем комнату
        if self.scope["user"].is_staff:
            room = ChatRoom.objects.get(id=self.room_id)
            # Сообщение от администратора помечается как прочитанное
            ChatMessage.objects.create(room=room, sender=self.scope['user'], message=message, is_read=True)
        else:
            # Создаем или получаем комнату для пользователя, если это не админ
            print(self.scope)
            room, _ = ChatRoom.objects.get_or_create(user_id=3)
            # Сообщения от пользователей сохраняются как непрочитанные
            ChatMessage.objects.create(room=room, sender=self.scope['user'], message=message, is_read=False)

    @database_sync_to_async
    def mark_messages_as_read(self, room_id):
        """
        Отмечаем все сообщения как прочитанные, если чат открыт.
        """
        room = ChatRoom.objects.get(id=room_id)
        room.messages.filter(is_read=False).update(is_read=True)

    # @database_sync_to_async
    # def send_previous_messages(self, room_id):
    #     """
    #     Отправляем предыдущие 50 сообщений.
    #     """
    #     room = ChatRoom.objects.get(id=room_id)
    #     messages = room.messages.all().order_by('-timestamp')[:50]
    #     return [{'sender': msg.sender.phone_number, 'message': msg.message, 'timestamp': msg.timestamp.isoformat()} for
    #             msg in messages]
