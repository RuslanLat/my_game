# admin_api/app/quiz/models.py

from dataclasses import dataclass
from typing import List, Optional
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey

from app.store.database.sqlalchemy_base import db


@dataclass
class Theme:

    """ Класс Theme используется для фомирования модели
    данных темы игры

    Attributes
    ----------
    id : int
        идентификатор темы
    title : str
        наименование темы
    lap: int
        раунд игры
    """

    id: Optional[int]
    title: str
    lap: int


@dataclass
class Question:

    """ Класс Question используется для фомирования модели
    данных вопроса игры

    Attributes
    ----------
    id : int
        идентификатор вопроса
    title : str
        содержание вопроса
    theme_id: int
        идентификатор темы
    answers: str
        ответ
    points: int
        количество баллов (очков)
    image_href: str
        ссылка на фото вопроса
    audio_href: str
        ссылка на аудио вопроса
    media_id: int
        идентификатор медиа в vk
    """

    id: Optional[int]
    title: str
    theme_id: int
    answers: str
    points: int
    image_href: Optional[str]
    audio_href: Optional[str]
    media_id: Optional[int]


class ThemeModel(db):

    """ Класс ThemeModel используется для фомирования модели
    данных темы в базе данных

    Attributes
    ----------
    id : int
        идентификатор темы
    title : str
        наименование темы
    lap : int
        раунд
    """

    __tablename__ = "themes"
    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True)
    lap = Column(Integer)
    question = relationship("QuestionModel")


class QuestionModel(db):

    """ Класс QuestionModel используется для фомирования модели
    вопроса в базе данных

    Attributes
    ----------
    id : int
        идентификатор вопроса
    title : str
        содержание вопроса
    theme_id: int
        идентификатор темы
    answers: str
        ответ
    points: int
        количество баллов (очков)
    image_href: str
        ссылка на фото вопроса
    audio_href:
        ссылка на аудио вопроса
    media_id: int
        идентификатор медиа в vk
    """

    __tablename__ = "questions"
    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True)
    # relationship: themes
    theme_id = Column(ForeignKey("themes.id" , ondelete="CASCADE"), nullable=False)
    answers = Column(String)
    points = Column(Integer)
    image_href = Column(String)
    audio_href = Column(String)
    media_id = Column(Integer)
