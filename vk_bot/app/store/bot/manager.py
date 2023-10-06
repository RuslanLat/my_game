from collections import defaultdict
import typing
from typing import Optional
import asyncio
from asyncio import Task
import time

if typing.TYPE_CHECKING:
    from app.web.app import Application

from app.store.vk_api.dataclasses import Message
from app.store.bot.game import Game


class BotManager:

    def __init__(self, app: "Application"):

        self.app = app
        self.is_running = False
        self.manager_task: Optional[Task] = None


    async def start(self):

        self.is_running = True
        asyncio.create_task(self.manager(), name="manager_task")

    async def stop(self):

        self.is_running = False
        if self.manager_task:
            await asyncio.wait([self.manager_task], timeout=30)

    async def pause(self):
        await asyncio.sleep(1)

    async def manager(self):
        while self.is_running:
            updates = await self.app.store.broker.consumer1()




            for update in updates:
                if update.type == "message_new":
                    params = await self.app.store.game.make_message(update)
                    if params:
                        for param in params:
                            await self.app.store.broker.producer2(param)
                                # time.sleep(4)
                                # await asyncio.create_task(self.pause())
                                
                if update.type == "message_event":

                    if update.object.message.get("payload").get("type") == "title":
                        params = await self.app.store.game.make_event(update)
                    else:
                        params = await self.app.store.game.make_event_question(update)
                        
                    await self.app.store.vk_api.send_message_event_answer(event=params)

                if update.type == "new" or update.type == "message_new" or update.type == "message_event":

                    if self.app.store.game.timer[2000000018]["status"] and (time.time() - self.app.store.game.timer[2000000018]["time"]) >= 15:
                        try:
                            data = list(self.app.store.game.points_list[2000000018].values())[0] + list(self.app.store.game.points_list[2000000018].values())[1]
                        except:
                            data = []
                        if len(data) == 8:
                            param_key = await self.app.store.game.stop_game_time(2000000018)
                            await self.app.store.game_accessor.update_status_game(2000000018)
                            param_end = await self.app.store.game.end_game_time(2000000018)
                            await self.app.store.broker.producer2(param_end)
                            await self.app.store.broker.producer2(param_key)
                        else:
                            select_player = self.app.store.game.select_player[2000000018]
                            time_params = await self.app.store.game.time_end(2000000018)
                            keybord_param = await self.app.store.game.game_process_time(2000000018, questions=self.app.store.game.questions_nuw[2000000018], points_list=self.app.store.game.points_list[2000000018])
                            await self.app.store.broker.producer2(time_params)
                            await self.app.store.broker.producer2(keybord_param)
                            await self.app.store.broker.producer2(select_player)
                            self.app.store.game.timer[2000000018]["status"] = False

                    if self.app.store.game.timer[2000000020]["status"] and (time.time() - self.app.store.game.timer[2000000020]["time"]) >= 15:
                        try:
                            data = list(self.app.store.game.points_list[2000000020].values())[0] + list(self.app.store.game.points_list[2000000020].values())[1]
                        except:
                            data = []
                        if len(data) == 8:
                            param_key = await self.app.store.game.stop_game_time(2000000020)
                            await self.app.store.game_accessor.update_status_game(2000000020)
                            param_end = await self.app.store.game.end_game_time(2000000020)
                            await self.app.store.broker.producer2(param_end)
                            await self.app.store.broker.producer2(param_key)
                        else:

                            select_player = self.app.store.game.select_player[2000000020]
                            time_params = await self.app.store.game.time_end(2000000020)
                            keybord_param = await self.app.store.game.game_process_time(2000000020, questions=self.app.store.game.questions_nuw[2000000020], points_list=self.app.store.game.points_list[2000000020])
                            await self.app.store.broker.producer2(time_params)
                            await self.app.store.broker.producer2(keybord_param)
                            await self.app.store.broker.producer2(select_player)
                            self.app.store.game.timer[2000000020]["status"] = False