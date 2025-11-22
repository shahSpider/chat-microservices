from asgiref.sync import async_to_sync, sync_to_async
import json
import jwt
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings
from urllib.parse import parse_qs


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("New WebSocket connection attempt")
        query_string = self.scope['query_string'].decode('utf-8')
        params = parse_qs(query_string)
        token = params.get('token', [None])[0] # token retrieved

        if token:
            try:
                decoded_data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
                self.user = await self.get_user(decoded_data['user_id']) # get the user from the token
                self.scope['user'] = self.user

            except jwt.ExpiredSignatureError:
                await self.close(code=4000) # close connection if token expired
                return
            except jwt.InvalidTokenError:
                await self.close(code=4001) # close connection if token invalid
                return
        else:
            await self.close(code=4002) # close connection if no token
            return

        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        self.room_group_name = f'chat_{self.conversation_id}'
        
        # Add channel to group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Accept the websocket connection
        await self.accept()

        user_data = await self.get_user_data(self.user)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'online_status',
                'online_users': [user_data],
                'status': 'online',
            }
        )
    async def disconnect(self, close_code):
        if hasattr(self, 'room_group'):
            # notify others about the disconnect
            user_data = await self.get_user_data(self.scope["user"])
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'online_status',
                    'online_users': [user_data],
                    'status': 'offline',
                }
            )

            # Remove channel from group
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        event_type = text_data_json.get('type')

        if event_type == 'chat_message':
            message_content = text_data_json.get('message')
            user_id = text_data_json.get('user')

            try:
                user = await self.get_user(user_id)
                conversation = await self.get_conversation(self.conversation_id)

                from .serializers import UserListSerializer
                user_data = UserListSerializer(user).data

                # save message to database
                message = await self.save_message(user, conversation, message_content)
                # broadcast message to group
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': message.content,
                        'user': user_data,
                        'timestamp': message.timestamp.isoformat(),

                    }
                )
            except Exception as e:
                print(f"Error saving message: {e}")
        
        elif event_type == 'typing':
            try:
                user_data = await self.get_user_data(self.scope["user"])
                receiver_id = text_data_json.get('receiver')

                if receiver_id is None:
                    if isinstance(receiver_id, (str, int, float)):
                        receiver_id = int(receiver_id)
                        
                        if receiver_id != self.scope["user"].id:
                            print(f"Typing event from user {self.scope['user'].id} to {receiver_id}")
                            await self.channel_layer.group_send(
                                self.room_group_name,
                                {
                                    'type': 'typing',
                                    'user': user_data,
                                    'receiver_id': receiver_id,
                                }
                            )
                        else:
                            print(f"{self.scope['user'].id} tried to send typing event to self.")
                    else:
                        print(f"Invalid receiver_id type: {type(receiver_id)}")
                else:
                    print(f"No receiver_id provided in typing event.")
            except ValueError as ve:
                print(f"Error parsing receiver ID: {ve}")
            except Exception as e:
                print(f"Error getting user data: {e}")

    async def chat_message(self, event):
        message = event['message']
        user = event['user']
        timestamp = event['timestamp']

        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': message,
            'user': user,
            'timestamp': timestamp,
        }))

    async def typing(self, event):
        user = event['user']
        receiver = event.get('receiver')
        is_typing = event.get('is_typing', False)

        await self.send(text_data=json.dumps({
            'type': 'typing',
            'user': user,
            'receiver': receiver,
            'is_typing': is_typing,
        }))

    async def online_status(self, event):
        await self.send(text_data=json.dumps(event))

    @sync_to_async
    def get_user(self, user_id):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        return User.objects.get(id=user_id)
    
    @sync_to_async
    def get_user_data(self, user):
        from .serializers import UserListSerializer
        return UserListSerializer(user).data
    
    @sync_to_async
    def get_conversation(self, conversation_id):
        from .models import Conversation
        try:
            return Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            print(f"Conversation with id {conversation_id} does not exist.")
            return None
    
    @sync_to_async
    def save_message(self, user, conversation, content):
        from .models import Message
        message = Message.objects.create(
            sender=user,
            conversation=conversation,
            content=content
        )
        return message
    
