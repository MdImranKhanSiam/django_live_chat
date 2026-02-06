import json
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from asgiref.sync import async_to_sync, sync_to_async
from django.contrib.auth.models import User
from . models import ChatMessage



class chat_consumer(WebsocketConsumer):
    def connect(self):
        self.room_group = 'test1'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group,
            self.channel_name
        )


        self.accept()

        # self.send(text_data=json.dumps({
        #     'msg_type' : 'Websocket connection successful',
        #     'message' : 'You are connected'
        # }))

    def receive(self, text_data):
        json_data = json.loads(text_data)
        the_message = json_data['Message']

        async_to_sync(self.channel_layer.group_send)(
            self.room_group,
            {
                'type' : 'chat_message',
                'message' : the_message
            }
        )

        

        # print(f'Message: {the_message}')

        # self.send(
        #     text_data=json.dumps(
        #         {
        #             'type' : 'check-receive',
        #             'Sent' : the_message,
        #         }
        #     )
        # )

    def chat_message(self, event):
        message = event['message']

        self.send(
            text_data=json.dumps(
                {
                    'type' : 'check-receive',
                    'sent' : message,
                }
            )
        )


class PrivateChatConsumer(AsyncWebsocketConsumer):

    # Initializing handshake
    async def connect(self):

        # Gets other users id from url
        self.other_user_id = self.scope['url_route']['kwargs']['user_id']
        
        # Gets current users id
        self.user = self.scope['user']

        # Stops anonymous connections, Without this anyone can connect
        if not self.user.is_authenticated:
            await self.close()
            return
        
        # Creates a string like chat_2_5 for dynamic shared room name
        # Sorted so that two users only have one room and not two
        user1 = str(self.user.id)
        user2 = str(self.other_user_id)
        list_of_users = [user1, user2]
        users = sorted(list_of_users)
        self.room_name = f"chat_{"_".join(users)}"

        # Registers this WebSocket connection to a group, so it can receive messages sent to that group
        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['typed_message']

        # Save the message to the database. Using await so that it doesn't block other users
        await self.save_message_to_database(message)

        # Broadcast a message to all channels that are currently in a group
        await self.channel_layer.group_send(
            self.room_name,
            {
                'type' : 'chat_message',
                'the_message' : message,
                'the_sender' : self.user.username,
            }
        )

    @sync_to_async
    def save_message_to_database(self, message):
        receiver = User.objects.get(id=self.other_user_id)

        ChatMessage.objects.create(
            sender = self.user,
            receiver = receiver,
            message = message
        )

    async def chat_message(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    'type' : 'private-chat',
                    'live_message' : event['the_message'],
                    'sender' : event['the_sender'],
                }
            )
        )

        