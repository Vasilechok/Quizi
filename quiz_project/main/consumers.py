from channels.generic.websocket import AsyncWebsocketConsumer
import json

class SessionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("connect start")

        try:
            self.code = self.scope['url_route']['kwargs']['code']
            self.group_name = f"session_{self.code}"

            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )

            await self.accept()
            print("accepted")
        except Exception as e: 
            print("error:", e)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def start_game(self, event):
        await self.send(text_data=json.dumps({
            "type": "start_game"
        }))