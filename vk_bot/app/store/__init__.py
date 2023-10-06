import typing

from app.store.database.database import Database

if typing.TYPE_CHECKING:
    from app.web.app import Application


class Store:

    def __init__(self, app: "Application"):

        from app.store.quiz.accessor import QuizAccessor
        from app.store.vk_api.accessor import VkApiAccessor
        from app.store.broker.accessor import BrokerAccessor
        from app.store.bot.manager import BotManager
        from app.store.sender.accessor import SenderManager
        from app.store.poller.poller import Poller
        from app.store.bot.game import Game
        from app.store.games.accessor import GameAccessor


        self.quizzes = QuizAccessor(app)
        self.vk_api = VkApiAccessor(app)
        self.broker = BrokerAccessor(app)
        self.sender = SenderManager(app)
        self.bot_manager = BotManager(app)
        self.poller = Poller(app)
        self.game = Game(app)
        self.game_accessor = GameAccessor(app)


def setup_store(app: "Application"):
    app.database = Database(app)
    app.on_startup.append(app.database.connect)
    app.on_cleanup.append(app.database.disconnect)
    app.store = Store(app)