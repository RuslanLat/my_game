# admin_api/app/web/mixins.py

from aiohttp_session import get_session
from aiohttp.abc import StreamResponse
from aiohttp.web_exceptions import HTTPUnauthorized, HTTPForbidden


class AuthRequiredMixin:

    """ Класс AuthRequiredMixin используется
    для переопределения View с целью валидации
    данных админа
    """

    async def _iter(self) -> StreamResponse:

        """ Функция переопределения View

        Raises:
            HTTPUnauthorized: не авторизован
            HTTPForbidden: не верные данные авторизации
            HTTPForbidden: не верные данные авторизации
            HTTPForbidden: не верные данные авторизации

        Returns:
            StreamResponse: результат итерации View
        """
        session = await get_session(self.request)
        if session.new:
            raise HTTPUnauthorized
        
        admin_data: dict = session.get("admin")
        if not admin_data:
            raise HTTPForbidden
        
        admin_email = admin_data.get("email")
        if not admin_email:
            raise HTTPForbidden

        admin = await self.store.admins.get_by_email(admin_email)
        if not admin:
            raise HTTPForbidden
        
        self.request.admin = admin # Admin(id=admin.id, email=admin.email, password=admin.password)
        
        return await super()._iter()
