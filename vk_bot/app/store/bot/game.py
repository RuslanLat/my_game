import asyncio
import time
from asyncio import Task
import json
import random
from app.store.bot.messages import Messages
from app.store.bot.keyboard import KeyboardGame
import typing
from collections import defaultdict
if typing.TYPE_CHECKING:
    from app.web.app import Application


class Game:
    

    def __init__(self, app: "Application"):
        
        self.messages = Messages()
        self.keyboard = KeyboardGame()
        self.app = app
        self.flag1 = defaultdict()
        # self.task1 : Task = None
        self.answer_is_player = defaultdict(dict)
        self.answer_no_player = defaultdict(dict)
        self.answer = defaultdict()
        self.questions_nuw = defaultdict()
        self.game_status = defaultdict()
        self.points_list = defaultdict(lambda: defaultdict(list))
        self.spam = defaultdict()
        self.spam2 = defaultdict()
        self.timer = {2000000018 : {"time": time.time(),
                                  "status" : False},
                      2000000020 : {"time": time.time(),
                                  "status" : False}}
        self.select_player = defaultdict(dict)



    async def make_message(self, update):
        
        if update.object.message.get("message").get("action"):
            if update.object.message.get("message").get("action").get("type") == "chat_invite_user":

                params_chat_invite_user = await self.chat_invite_user(update)

                param_is_admin = await self.is_admin(update)
            
                return [params_chat_invite_user, param_is_admin]
        
        elif "Правила игры" in update.object.message.get("message").get("text"):

            params = await self.game_ruless(update)

            return [params]
        
        elif "Начать игру" in update.object.message.get("message").get("text"):

            peer_id = update.object.message.get("message").get("peer_id")

            self.flag1[peer_id] = True

            self.spam2[peer_id] = False
            self.spam[peer_id] = None


            # self.timer[peer_id] = {"time": 0,
            #                         "status" : False}

            param_start_game = await self.start_game(update)

            param_game_process = await self.game_process(update)

            self.game_status[peer_id] = True

            self.select_player[peer_id] = param_start_game[1]

            return [param_start_game[0], param_game_process, param_start_game[1]]
        
        elif "Стоп игра" in update.object.message.get("message").get("text"):

            peer_id = update.object.message.get("message").get("peer_id")

            self.game_status[peer_id] = False

            param = await self.stop_game(update)

            self.points_list[peer_id] = defaultdict(list)


            await self.app.store.game_accessor.update_status_game(peer_id)


            return [param]

        elif "Турнирная таблица" in update.object.message.get("message").get("text"):

            param = await self.game_result(update)

            return [param]
        
        elif "Назначен" in update.object.message.get("message").get("text"):
            # peer_id = update.object.message.get("peer_id")
            # param = {"peer_id" : peer_id}
            # profiles = await self.app.store.vk_api.get_conversation_members(param)
            # await self.app.store.game_accessor.create_players(profiles)

            params = await self.game_preview(update)

            return [params]
        
        elif update.object.message.get("message").get("payload") and self.game_status[update.object.message.get("message").get("peer_id")]:
            
            param = await self.question_make(update)

            self.timer[update.object.message.get("message").get("peer_id")] = {"time": time.time(),
                                                                               "status" : True}

            return [param]
        
        elif "Ответить" in update.object.message.get("message").get("text") and self.flag1[update.object.message.get("message").get("peer_id")] and self.game_status[update.object.message.get("message").get("peer_id")]:

            self.spam[update.object.message.get("message").get("peer_id")] = update.object.message.get("message").get("from_id")

            self.spam2[update.object.message.get("message").get("peer_id")] = True

            self.timer[update.object.message.get("message").get("peer_id")] = {"time": time.time(),
                                                                               "status" : False}

            params_answer = await self.answer_is(update)

            peer_id = update.object.message.get("message").get("peer_id")

            self.answer_is_player[peer_id] = {"message" : "Не ваша очередь отвечать",
                              "peer_id" : peer_id}

            self.flag1[peer_id] = False

            self.answer_no_player[peer_id] = await self.get_player(update)

            self.select_player[peer_id] = self.answer_no_player[peer_id]
            
                  
            # self.task1 = asyncio.create_task(self.pause(update))

            # await asyncio.gather(self.task1)
            
            return [params_answer]
        
        elif "Ответить" in update.object.message.get("message").get("text") and not self.flag1[update.object.message.get("message").get("peer_id")] and self.game_status[update.object.message.get("message").get("peer_id")]:

            params_answer =  self.answer_is_player[update.object.message.get("message").get("peer_id")]
            
            return [params_answer]
        
        
        elif update.object.message.get("message").get("text") and self.game_status[update.object.message.get("message").get("peer_id")] \
            and update.object.message.get("message").get("from_id") == self.spam[update.object.message.get("message").get("peer_id")] \
            and self.spam2[update.object.message.get("message").get("peer_id")]:

            points = self.answer[update.object.message.get("message").get("peer_id")]["points"]

            self.spam[update.object.message.get("message").get("peer_id")] = None
            self.spam2[update.object.message.get("message").get("peer_id")] = False

            try:
                peer_id = update.object.message.get("message").get("peer_id")

                data = list(self.points_list[peer_id].values())[0] + list(self.points_list[peer_id].values())[1]
            except:
                data = []
            
            if update.object.message.get("message").get("text").lower() in self.answer[update.object.message.get("message").get("peer_id")]["answers"].lower():
                  
                await self.app.store.game_accessor.update_points(peer_id=update.object.message.get("message").get("peer_id"),
                                                                 vk_id=update.object.message.get("message").get("from_id"),
                                                                  points=points)

                param = await self.answer_true(update, points)

                param_player = await self.get_player(update)

                param_quest = await self.game_process_new(update, questions=self.questions_nuw[peer_id], points_list=self.points_list[peer_id])


                self.flag1[peer_id] = True

                if len(data) == 8:

                    peer_id = update.object.message.get("message").get("peer_id")
                
                    self.game_status[peer_id] = False
                    param_key = await self.stop_game(update)
                    
                    self.points_list[peer_id] = defaultdict(list)

                    await self.app.store.game_accessor.update_status_game(peer_id)

                    self.timer = {2000000018 : {"time": time.time(),
                                  "status" : False},
                      2000000020 : {"time": time.time(),
                                  "status" : False}}

                    param_end = await self.end_game(update)

                    return [param, param_end, param_key]

                

                return [param, param_quest, param_player]
            else:
                await self.app.store.game_accessor.update_points(peer_id=update.object.message.get("message").get("peer_id"),
                                                                 vk_id=update.object.message.get("message").get("from_id"),
                                                                  points=-points)

                param = await self.answer_false(update, -points)

                param_player = await self.get_player(update)

                param_quest = await self.game_process_new(update, questions=self.questions_nuw[peer_id], points_list=self.points_list[peer_id])

                self.flag1[peer_id] = True

                if len(data) == 8:

                    peer_id = update.object.message.get("message").get("peer_id")
                    self.game_status[peer_id] = False
                    param_key = await self.stop_game(update)
                    
                    self.points_list[peer_id] = defaultdict(list)

                    await self.app.store.game_accessor.update_status_game(peer_id)

                    param_end = await self.end_game(update)

                    self.timer = {2000000018 : {"time": time.time(),
                                  "status" : False},
                      2000000020 : {"time": time.time(),
                                  "status" : False}}

                    return [param, param_end, param_key]

                return [param, param_quest, param_player]
        
        else:
            return None


    async def make_event(self, update):


        params = {"event_id" : update.object.message.get("event_id"),
                 "peer_id" : update.object.message.get("peer_id"),
                 "user_id" : update.object.message.get("user_id"),
                 "event_data" : str(json.dumps({"type": "show_snackbar",
                                 "text": "Выбирете вопрос темы по количеству очков"}))}
        
        return params


    async def make_event_question(self, update):


        params = {"event_id" : update.object.message.get("event_id"),
                 "peer_id" : update.object.message.get("peer_id"),
                 "user_id" : update.object.message.get("user_id"),
                 "event_data" : str(json.dumps({"type": "show_snackbar",
                                 "text": "Этот вопрос уже выбран"}))}
        
        return params


    async def chat_invite_user(self, update):

        
        params = {"message" : await self.messages.game_rules(),
                 "keyboard" : await self.keyboard.menu_in_start(),
                 "peer_id" : update.object.message.get("message").get("peer_id")}
        
        return params
    
    async def game_ruless(self, update):
           
        params = {"message" : await self.messages.game_rules(),
                "peer_id" : update.object.message.get("message").get("peer_id")}
        
        return params
    
    async def end_game(self, update):
           
        params = {"message" : await self.messages.end_game(),
                "peer_id" : update.object.message.get("message").get("peer_id")}
        
        return params
    

    async def end_game_time(self, peer_id):
           
        params = {"message" : await self.messages.end_game(),
                "peer_id" : peer_id}
        
        return params
    
    
    async def start_game(self, update):

        theme_titles = await self.app.store.quizzes.list_themes()

        peer_id = update.object.message.get("message").get("peer_id")

        game = await self.app.store.game_accessor.create_game(peer_id)


        param = {"peer_id" : peer_id} 

        profiles = await self.app.store.vk_api.get_conversation_members(param)

        for profile in profiles:
            vk_id = profile.vk_id
            if not  await self.app.store.game_accessor.get_player_by_id(vk_id):
                await self.app.store.game_accessor.create_player(profile)
        
        await self.app.store.game_accessor.create_game_session(game_id=game.id, players=profiles)
    
        profile = random.choice(profiles)


        params_start = {"message" : await self.messages.themes(theme_titles),
                "peer_id" : peer_id,
                "keyboard" : await self.keyboard.menu_in_game()}
        

        params_select = {"message" : await self.messages.select_question(profile),
                         "peer_id" : peer_id}
        
        return [params_start, params_select]
    

    async def get_player(self, update):


        profile = await self.app.store.game_accessor.get_player_by_id(update.object.message.get("message").get("from_id"))


        params_select = {"message" : await self.messages.select_question(profile),
                         "peer_id" : update.object.message.get("message").get("peer_id")}
        
        return params_select


    

    async def game_preview(self, update):


        params = {"message" : await self.messages.start_game(),
                "peer_id" : update.object.message.get("message").get("peer_id")}
        
        return params
    

    async def stop_game(self, update):

        peer_id = update.object.message.get("message").get("peer_id")

        leader_board = await self.app.store.game_accessor.get_leader_board(peer_id)


        params = {"message" : await self.messages.game_leader_board(leader_board),
                "peer_id" : peer_id,
                "keyboard" : await self.keyboard.menu_in_start()}
        
        return params
    
    async def stop_game_time(self, peer_id):

        self.timer[peer_id] = {"time": time.time(), "status" : False}

        self.points_list[peer_id] = defaultdict(list)

        leader_board = await self.app.store.game_accessor.get_leader_board(peer_id)


        params = {"message" : await self.messages.game_leader_board(leader_board),
                "peer_id" : peer_id,
                "keyboard" : await self.keyboard.menu_in_start()}
        
        return params


    async def game_result(self, update):

        peer_id = update.object.message.get("message").get("peer_id")

        leader_board = await self.app.store.game_accessor.get_leader_board(peer_id)

    
        params = {"message" : await self.messages.game_leader_board(leader_board),
                  "peer_id" : peer_id}
        
        return params


    async def game_process(self, update):

        theme_titles = await self.app.store.quizzes.list_themes(lap=1)
        theme_id = [theme.id for theme in theme_titles]
        #theme_raund = random.sample(theme_id, k=2)
        random.shuffle(theme_id )
        theme_raund = theme_id[:2]

        questions = await self.app.store.quizzes.list_questions_lap(theme_raund)

        peer_id = update.object.message.get("message").get("peer_id")


        self.questions_nuw[peer_id] = questions


        params = {"message" : "Вопросы 1 раунда",
                  "peer_id" : peer_id,
                  "keyboard" : await self.keyboard.question_lap(questions)}
        
        return params
    
    async def game_process_new(self, update, questions, points_list):


        
        params = {"message" : "Вопросы 1 раунда",
                  "peer_id" : update.object.message.get("message").get("peer_id"),
                  "keyboard" : await self.keyboard.question_lap_apdate(questions, points_list)}
        
        return params
    

    async def game_process_time(self, peer_id, questions, points_list):


        
        params = {"message" : "Вопросы 1 раунда",
                  "peer_id" : peer_id,
                  "keyboard" : await self.keyboard.question_lap_apdate(questions, points_list)}
        
        return params
    
    async def is_admin(self, update):

        params = {"message" : await self.messages.is_admin(),
                  "peer_id" : update.object.message.get("message").get("peer_id"),
                  "keyboard" : await self.keyboard.is_admin()}
        
        return params
    
    async def question_make(self, update):

        param = eval(update.object.message.get("message").get("payload"))

        peer_id = update.object.message.get("message").get("peer_id")

        question = await self.app.store.quizzes.get_question_by_id(param.get("id"), param.get("points"))

        self.points_list[peer_id][param.get("title")].append(param.get("points"))


        params = {"message" : param.get("title") + " " + str(param.get("points")) + "%0a%0a" + question.title + "%0a%0a",
                  "peer_id" : peer_id,
                  "keyboard" : await self.keyboard.question()}
        
        self.answer[peer_id] = {"points": param.get("points"),
                                "answers": question.answers}
        

        if question.image_href:
            
            params.update({"attachment": f"photo-204178645_{question.media_id}"})

        if question.audio_href:
            
            params.update({"attachment": f"audio52428910_{question.media_id}"})

        return params
    

    async def answer_is(self, update):

        player = await self.app.store.game_accessor.get_player_by_id(update.object.message.get("message").get("from_id"))

        params = {"message" : await self.messages.answer_action(player),
                  "peer_id" : update.object.message.get("message").get("peer_id")}
        
        return params
    
    async def pause_question(self, update):
        await asyncio.sleep(5)

        params_time = await self.time_end(update)

        return params_time


    async def time_end(self, peer_id):


        params = {"message" : "Время для ответа ВЫШЛО",
                  "peer_id" : peer_id}
        
        return params
    
    async def answer_true(self, update, points):


        params = {"message" : await self.messages.answer_true(points),
                  "peer_id" : update.object.message.get("message").get("peer_id")}
        
        return params
    
    async def answer_false(self, update, points):


        params = {"message" : await self.messages.answer_false(points),
                  "peer_id" : update.object.message.get("message").get("peer_id")}
        
        return params