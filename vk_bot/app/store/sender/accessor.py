import typing
from typing import Optional
import asyncio
from asyncio import Task


if typing.TYPE_CHECKING:
    from app.web.app import Application


class SenderManager:

    def __init__(self, app: "Application"):

        self.app = app
        self.is_running = False
        self.sender_task: Optional[Task] = None


    async def start(self):

        self.is_running = True
        asyncio.create_task(self.sender(), name="sender_task")

    async def stop(self):

        self.is_running = False
        if self.sender_task:
            await asyncio.wait([self.sender_task], timeout=10)




    async def sender(self):

        while self.is_running:

            params = await self.app.store.broker.consumer2()

            await self.app.store.vk_api.send_message(param=params)
