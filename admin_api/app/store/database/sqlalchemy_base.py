# admin_api/app/store/sqlalchemy_base.py

from sqlalchemy.orm import declarative_base

# определение конфигурации для взаимодействия с базой данных
db = declarative_base()