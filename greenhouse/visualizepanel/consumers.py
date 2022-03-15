import json
from random import randint
from asyncio import sleep
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings

class WSConsumer(AsyncWebsocketConsumer):

    group_name = settings.STREAM_SOCKET_GROUP_NAME

    async def connect(self):
        # Joining group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()
        # for i in range(100):
        #     await self.send(json.dumps({ 'message':randint(1, 100) }))
        #     await sleep(1)

    async def disconnect(self, close_code):
        # Leave group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        print(text_data)
        # Print message that receive from Websocket

        # Send data to group
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'system_load',
                'data': text_data
            }
        )

    async def system_load(self, event):
        # Receive data from group
        print('sending message to client')
        jsondata = json.loads(event['data'])
        await self.send(text_data=json.dumps(jsondata))
    

