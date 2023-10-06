# admin_api/app/admin/views.py

from aiohttp.web import HTTPForbidden, HTTPUnauthorized
from aiohttp_apispec import docs, request_schema, response_schema
from aiohttp_session import new_session
from aiohttp.web_response import Response

from app.admin.schemes import AdminSchema, AdminLoginSchema
from app.web.app import View
from app.web.utils import json_response
from app.web.mixins import AuthRequiredMixin


class AdminLoginView(View):

    """ Класс AdminLoginView используется для 
    представления формы регистрации админа в API
    """

    @request_schema(AdminLoginSchema)
    @response_schema(AdminSchema, 200)
    @docs(tags=["admin"], summary="Add admin login view", description="Get admin from database")
    async def post(self) -> Response:

        """ Метод авторизации админа в API

        Args:
            email (str): электронный адрес админа
            password (str): пароль админа

        Raises:
            HTTPForbidden: не верные данные авторизации

        Returns:
            Response: данные админа
        """

        email = self.data["email"]
        password: str = self.data["password"]
        
        admin = await self.store.admins.get_by_email(email)
        
        if not admin or not admin.is_password_valid(password):
            raise HTTPForbidden
        
        admin_data = AdminSchema().dump(admin)

        session = await new_session(request=self.request)

        session["admin"] = admin_data

        return json_response(data=admin_data)


class AdminCurrentView(View):

    """ Класс AdminCurrentView используется для 
    представления данных админа при входе в API
    """

    @response_schema(AdminSchema, 200)
    @docs(tags=["admin"], summary="Add admin current view", description="Current admin from session")
    async def get(self) -> Response:

        """ Метод получения корректного админа

        Returns:
            Response: данные админа
        """

        if not self.request.admin:
            raise HTTPUnauthorized
        
        raw_admin = AdminSchema().dump(self.request.admin)

        return json_response(raw_admin)
    

class AdminAddView(View):

    """ Класс AdminAddView используется для 
    представления формы добавления админа
    в базу данных
    """

    @request_schema(AdminLoginSchema)
    @response_schema(AdminSchema, 200)
    @docs(tags=["admin"], summary="Add admin add view", description="Add admin in database")
    async def post(self) -> Response:

        """ Метод добавления админа в базу данных
        (используется для теста API)

        Args:
            email (str): электронный адрес админа
            password (str): пароль админа

        Returns:
            Response: данные админа
        """        

        email = self.data["email"]
        password: str = self.data["password"]
        
        raw_admin = await self.store.admins.create_admin(email=email, password=password)

        admin = AdminSchema().dump(raw_admin)

        return json_response(data=admin)