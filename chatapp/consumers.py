import json

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from .models import Message

class chatconsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.sender=self.scope['user'].id
        self.receiver=self.scope['url_route']['kwargs']['receiver']

        if int(self.sender) > int(self.receiver):
            self.room_name=f'{self.sender}--{self.receiver}'
        else:
            self.room_name=f'{self.receiver}--{self.sender}'

        self.group_room_name='chat_%s' % self.room_name

        print(self.group_room_name)
        await self.channel_layer.group_add(
            self.group_room_name,
            self.channel_name
        )

        await self.accept()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_room_name,
            self.channel_name
        )
        
    async def receive(self,text_data):
        data=json.loads(text_data)
        print(data)

        message=data['message']
        sender=data['sender']
        receiver=data['receiver']

        await self.save_message(sender,receiver,message)

        await self.channel_layer.group_send(
            self.group_room_name,
            {
                'type': 'chat.message',
                'message': message,
                'sender': sender
            }
        )

    async def chat_message(self,event):
        message=event['message']
        sender=event['sender']

        await self.send(text_data=json.dumps({
            'message':message,
            'sender':sender
        }))

    @sync_to_async
    def save_message(self,sender,receiver,message):
        sender=User.objects.get(id=sender)
        receiver=User.objects.get(id=receiver)

        Message.objects.create(sender=sender,receiver=receiver,message=message)