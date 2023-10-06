import typing
from typing import Optional
import asyncio
from asyncio import Task
#asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

if typing.TYPE_CHECKING:
    from app.web.app import Application


class Poller:

    def __init__(self, app: "Application"):

        self.app = app
        self.is_running = False
        self.poller_task: Optional[Task] = None


    async def start(self):

        self.is_running = True
        asyncio.create_task(self.poller(), name="poller_task")

    async def stop(self):

        self.is_running = False
        if self.poller_task:
            await asyncio.wait([self.poller_task], timeout=10)

    async def poller(self):

        while self.is_running:
            updates = await self.app.store.vk_api.poll()
            await self.app.store.broker.producer1(updates)