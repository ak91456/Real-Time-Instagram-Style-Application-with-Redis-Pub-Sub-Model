import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
class NotificationsConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        if self.scope['user'].is_anonymous:
            await self.close()
            return
        self.user = self.scope['user']
        self.group_name = f'notifications_user_{self.user.id}'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
    async def disconnect(self, close_code):
        try:
            await self.channel_layer.group_discard(self.group_name, self.channel_name)
        except Exception:
            pass
    async def notification_message(self, event):
        payload = event.get('payload')
        await self.send_json(payload)
