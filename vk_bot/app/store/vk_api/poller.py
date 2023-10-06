from asyncio import Task
import asyncio
from typing import Optional

from app.store import Store
#asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

class Poller:
    def __init__(self, store: Store):
        self.store = store
        self.is_running = False
        self.poll_task: Optional[Task] = None

    async def start(self):
        # TODO: добавить asyncio Task на запуск poll
        # raise NotImplementedError
        self.is_running = True
        asyncio.create_task(self.poll())

    async def stop(self):
        # TODO: gracefully завершить Poller
        # raise NotImplementedError
        self.is_running = False
        if self.poll_task:
            await asyncio.wait([self.poll_task], timeout=30)
    async def poll(self):
        # raise NotImplementedError
        while self.is_running:
            updates = await self.store.vk_api.poll()
            await self.store.bots_manager.handle_updates(updates)
