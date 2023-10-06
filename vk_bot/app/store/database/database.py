from typing import Any, Optional, TYPE_CHECKING
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine, AsyncSession
from sqlalchemy.orm import declarative_base
from sqlalchemy.engine.url import URL

from app.store.database.sqlalchemy_base import db

if TYPE_CHECKING:
    from app.web.app import Application


class Database:

    """ Класс Database используется для определени
    акцессора для взаимодействия с базой данных
    """

    def __init__(self, app: "Application"):
        self.app = app
        self._engine: Optional[AsyncEngine] = None
        self._db: Optional[declarative_base] = None
        self.session: Optional[async_sessionmaker[AsyncSession]] = None

    async def connect(self, *_: list, **__: dict) -> None:

        """ Функция создания подключения к базе данных
        """

        self._db = db

        # создания объекта подключения
        self._engine = create_async_engine(
            URL.create(drivername="postgresql+asyncpg",
                        host=self.app.config.database.host,
                        database=self.app.config.database.database,
                        username=self.app.config.database.user,
                        password=self.app.config.database.password,
                        port=self.app.config.database.port,)
                        )
        
        # создание сессии
        self.session = async_sessionmaker(
            autoflush=True,
            bind=self._engine,
            expire_on_commit=False,
            class_=AsyncSession,
            )


    async def disconnect(self, *_: Any, **__: Any) -> None:

        """ Функция закрытия подключения к базе данных
        """

        try:
            await self._engine.dispose()
        except:
            pass