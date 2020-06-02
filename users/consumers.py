from channels.consumer import AsyncConsumer


class NotificationConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        print("websocket connected", event)

        await self.send({
            "type": "websocket.accept"
        })

    async def websocket_receive(self, event):
        print("websocket message received", event)

    async def websocket_disconnect(self, event):
        print("websocket disconnect", event)