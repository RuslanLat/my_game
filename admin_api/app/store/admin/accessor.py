# admin_api/app/store/admin/accessor.py

import typing
from typing import Optional
from hashlib import sha256
from sqlalchemy import select

from app.admin.models import Admin, AdminModel
from app.base.base_accessor import BaseAccessor

if typing.TYPE_CHECKING:
    from app.web.app import Application


class AdminAccessor(BaseAccessor):

    """ Класс AdminAccessor используется для 
    взаимодействия с базой данных
    """

    async def get_by_email(self, email: str) -> Optional[Admin]:

        """ Функция получения админа из базы данных 
        по его электронному адресу

        Args:
            email (str): электронный адрес админа

        Returns:
            Optional[Admin]: корректный админ
        """
        
        async with self.app.database.session() as session:
            query = select(AdminModel).where(AdminModel.email == email)
            admin: Optional[AdminModel] = await session.scalar(query)
        
        if not admin:
            return None

        return Admin(id=admin.id, email=admin.email, password=admin.password)

    async def create_admin(self, email: str, password: str) -> Admin:

        """ Функция создания замиси данных админа
        в базу данных

        Args:
            email (str): электронный адрес админа
            password (str): пароль админа

        Returns:
            Admin: данные админа в базе данных
        """

        new_admin = AdminModel(email=email, password=self.encode_password(password))

        async with self.app.database.session.begin() as session:
            session.add(new_admin)

        return Admin(id=new_admin.id, email=new_admin.email)

    def encode_password(self, password: str) -> str:

        """ Функция хэширования пароля админа

        Args:
            password (str): пароль админа

        Returns:
            str: хэшированый пароль админа
        """

        return sha256(password.encode()).hexdigest()
    
    def copmare_passwords(self, existing_admin: Admin, password: str) -> bool:

        """ Функция валидации пароля админа

        Args:
            existing_admin (Admin): данные админа
            password (str): пароль админа

        Returns:
            bool: результат валидации
        """
        
        return existing_admin.password == self.encode_password(password)
