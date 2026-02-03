import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

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