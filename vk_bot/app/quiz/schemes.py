# vk_bot/app/quiz/schemes.py

from marshmallow import Schema, fields


class ThemeSchema(Schema):

    """ Класс ThemeSchema используется для фомирования модели
    валидации данных темы вопроса

    Attributes
    ----------
    title : str
        наименование темы
    lap : int
        раунд игры
    """

    # id = fields.Int(required=False)
    title = fields.Str(required=True)
    lap = fields.Int(required=True)


class ThemeRequestSchema(ThemeSchema):

    """ Класс ThemeRequestSchema используется для фомирования модели
    валидации данных темы вопроса при запросе

    Attributes
    ----------
    title : str
        наименование темы
    lap : int
        раунд игры
    """
    pass


class ThemeResponseSchema(ThemeSchema):

    """ Класс ThemeResponseSchema используется для фомирования модели
    валидации данных темы вопроса при ответе

    Attributes
    ----------
    title : str
        наименование темы
    lap : int
        раунд игры
    """

    id = fields.Int(required=True)


class ThemeListResponseSchema(Schema):

    """ Класс ThemeListResponseSchema используется для фомирования модели
    валидации данных  списка тем вопросов при ответе

    Attributes
    ----------
    themes : List[ThemeResponseSchema]
        список тем 
    """

    themes = fields.Nested(ThemeResponseSchema, many=True)


class ThemeListRequestQuerySchema(Schema):

    """ Класс ThemeListRequestQuerySchema используется для фомирования модели
    валидации данных списка тем при запросе с учетом 
    раунда игры

    Attributes
    ----------
    lap : int
        раунд игры
    """

    lap = fields.Int()


class QuestionSchema(Schema):

    """ Класс QuestionSchema используется для фомирования модели
    валидации данных вопроса

    Attributes
    ----------
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
        идентификатор медиа файла в vk
    """

    title = fields.Str(required=True)
    theme_id = fields.Int(required=True)
    answers = fields.Str(required=True)
    points = fields.Int(required=True)
    image_href = fields.Str(required=False)
    audio_href = fields.Str(required=False)
    media_id = fields.Int(required=False)


class QuestionRequestSchema(QuestionSchema):

    """ Класс QuestionRequestSchema используется для фомирования модели
    валидации данных вопроса при запросе

    Attributes
    ----------
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
        идентификатор медиа файла в vk
    """

    pass


class QuestionResponseSchema(QuestionSchema):

    """ Класс QuestionSchema используется для фомирования модели
    валидации данных вопроса при ответе

    Attributes
    ----------
    id: int
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
        идентификатор медиа файла в vk
    """

    id = fields.Int(required=True)


class QuestionListResponseSchema(Schema):

    """ Класс QuestionListResponseSchema используется для фомирования модели
    валидации данных  списка вопросов при ответе

    Attributes
    ----------
    questions : List[QuestionResponseSchema]
        список вопросов
    """
    
    questions = fields.Nested(QuestionResponseSchema, many=True)


class QuestionListRequestQuerySchema(Schema):

    """ Класс QuestionListRequestQuerySchema используется для фомирования модели
    валидации данных списка вопросов при ответе с учетом 
    идентификатора темы

    Attributes
    ----------
    theme_id : int
        идентификатор темы
    """

    theme_id = fields.Int()