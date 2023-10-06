import asyncio
import random
import typing
from typing import Optional

from aiohttp.client import ClientSession

from app.base.base_accessor import BaseAccessor
from app.store.vk_api.dataclasses import Message, Update, UpdateObject, Members
#from app.store.vk_api.poller import Poller
#asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
if typing.TYPE_CHECKING:
    from app.web.app import Application


class VkApiAccessor(BaseAccessor):
    def __init__(self, app: "Application", *args, **kwargs):
        super().__init__(app, *args, **kwargs)
        self.session: Optional[ClientSession] = None
        self.key: Optional[str] = None
        self.server: Optional[str] = None
        self.ts: Optional[int] = None

    async def connect(self, app: "Application"):

        self.session = ClientSession()
        await self._get_long_poll_service()


    async def disconnect(self, app: "Application"):

        if self.session:
            await self.session.close()


    @staticmethod
    def _build_query(host: str, method: str, params: dict) -> str:
        url = host + method + "?"
        if "v" not in params:
            params["v"] = "5.131"
        url += "&".join([f"{k}={v}" for k, v in params.items()])
        return url

    async def _get_long_poll_service(self):
        bot_config = self.app.config.bot
        group_id = bot_config.group_id
        token = bot_config.token

        query = self._build_query(
            'https://api.vk.com/',
            'method/groups.getLongPollServer',
            {'group_id': group_id, 
             'access_token': token}
        )

        async with self.session.get(query) as response:
            resposen_body = await response.json()
            self.logger.info(resposen_body)
            data = resposen_body['response']
            self.key = data['key']
            self.server = data['server']
            self.ts = data['ts']

        return None


    async def poll(self):
        query = self._build_query(
            self.server, '',
            {
                'act': 'a_check',
                'key': self.key,
                'wait': 25,
                'mode': 2,
                'ts': self.ts
            }
        )

        async with self.session.get(query) as response:
            data = await response.json()
            self.logger.info(data)
            self.ts = data['ts']

        if len(data['updates']) != 0:

            return [
                Update(
                    type=u['type'],
                    group_id=u['group_id'],
                    object=UpdateObject(
                    message=u['object']
                    )) for u in data['updates'] if u['type'] == 'message_new' or 'message_event'
            ]
        else:
            return [Update(
                    type='new',
                    group_id=204178645,
                    object=UpdateObject(
                    message={}
                    ))]


    async def send_message(self, param) -> None:

        params = {"access_token": self.app.config.bot.token,
                "random_id": random.randint(1, 777777)}
        
        params.update(param)

        query = self._build_query(
            host="https://api.vk.com/",
            method="method/messages.send",
            params=params)

        async with self.session.get(query) as response:
            data = await response.json()
            self.logger.info(data)

        return None
    
    async def get_conversation_members(self, param) -> None:

        params = {"access_token": self.app.config.bot.token,
                  "group_id" : self.app.config.bot.group_id}
        
        params.update(param)

        query = self._build_query(
            host="https://api.vk.com/",
            method="method/messages.getConversationMembers",
            params=params)

        async with self.session.get(query) as response:
            data = await response.json()
            profiles = data["response"]["profiles"]

        return [
            Members(vk_id=profile.get("id"),
                    first_name=profile.get("first_name"),
                    last_name=profile.get("last_name"))
                    for profile in profiles]



    async def send_message_event_answer(self, event) -> None:
        query = self._build_query(
            host='https://api.vk.com/',
            method='method/messages.sendMessageEventAnswer',
            params={
                'event_id': event["event_id"],
                'access_token': self.app.config.bot.token,
                'user_id' : event["user_id"],
                'peer_id': event["peer_id"],
                'event_data' : event["event_data"]}
        )

        async with self.session.get(query) as response:
            data = await response.json()
            self.logger.info(data)

        return None


    # async def send_message(self, message: Message) -> None:
    #     query = self._build_query(
    #         host='https://api.vk.com/',
    #         method='method/messages.send',
    #         params={
    #             'message': message.text,
    #             'access_token': self.app.config.bot.token,
    #             'random_id': random.randint(1, 777777),
    #             'peer_id': message.peer_id,
    #         }
    #     )

    #     async with self.session.get(query) as response:
    #         data = await response.json()
    #         self.logger.info(data)

    #     return None