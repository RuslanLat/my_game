# admin_api/app/admin/schemes.py

from marshmallow import Schema, fields


# class AdminSchema(Schema):
#     id = fields.Int(required=False)
#     email = fields.Str(required=True)
#     password = fields.Str(required=True, load_only=True)


class AdminSchema(Schema):

    """ Класс AdminSchema используется для фомирования модели
    валидации данных админа при успешном входе в API

    Attributes
    ----------
    id : int
        идентификатор админа
    email : str
        электронный адрес админа
    """

    id = fields.Int()
    email = fields.Email()


class AdminLoginSchema(Schema):

    """ Класс AdminLoginSchema используется для фомирования модели
    валидации данных админа при входе в API

    Attributes
    ----------
    email : str
        электронный адрес админа
    password : str
        пароль админа
    """

    email = fields.Str(required=True)
    password = fields.Str(required=True)