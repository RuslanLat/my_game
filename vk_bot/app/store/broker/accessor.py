import asyncio
import typing

if typing.TYPE_CHECKING:
    from app.web.app import Application

from app.base.base_accessor import BaseAccessor

#asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


class BrokerAccessor(BaseAccessor):

    def __init__(self, app: "Application", *args, **kwargs):
        super().__init__(app, *args, **kwargs)

        self.queue1 = None
        self.queue2 = None


    async def connect(self, app: "Application"):

        self.queue1 = asyncio.Queue()
        self.queue2 = asyncio.Queue()
        await asyncio.gather(self.app.store.poller.start(), self.app.store.bot_manager.start(), self.app.store.sender.start())

    async def disconnect(self, app: "Application"):


        if self.app.store.poller:
            await self.app.store.poller.stop()

        if self.app.store.bot_manager:
            await self.app.store.bot_manager.stop()

        if self.app.store.sender:
            await self.app.store.sender.stop()


    async def producer1(self, updates):
        await self.queue1.put(updates)

    async def consumer1(self):

        updates = await self.queue1.get()
        
        return updates
    
    async def producer2(self, message):
        await self.queue2.put(message)


    async def consumer2(self):

        message = await self.queue2.get()

        return message