# admin_api/app/admin/models.py

from dataclasses import dataclass
from hashlib import sha256
from typing import Optional
from sqlalchemy import Column, Integer, String

from app.store.database.sqlalchemy_base import db


@dataclass
class Admin:

    """ Класс Admin используется для фомирования модели
    данных админа

    Attributes
    ----------
    id : int
        идентификатор админа
    email : str
        электронный адрес админа
    password : str
        пароль админа
    """

    id: int
    email: str
    password: Optional[str] = None

    def is_password_valid(self, password: str) -> bool:

        """ Функция валидации пароля админа

        Args:
            password (str): пароль админа

        Returns:
            bool: результат валидации
        """

        return self.password == sha256(password.encode()).hexdigest()

    @classmethod
    def from_session(cls, session: Optional[dict]) -> Optional["Admin"]:

        """ Метод получения данных сессии

        Args:
            session (Optional[dict]): данные сессии

        Returns:
            Optional["Admin"]: данные сессии админа
        """

        return cls(id=session["admin"]["id"], email=session["admin"]["email"])


class AdminModel(db):

    """ Класс AdminModel используется для фомирования модели
    данных админа в базе данных

    Attributes
    ----------
    id : int
        идентификатор админа
    email : str
        электронный адрес админа
    password : str
        пароль админа
    """

    __tablename__ = "admins"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    password = Column(String)