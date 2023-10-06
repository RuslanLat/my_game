# admin_api/app/web/config.py

import typing
import yaml
from dataclasses import dataclass

if typing.TYPE_CHECKING:
    from app.web.app import Application


@dataclass
class SessionConfig:
    key: str


@dataclass
class AdminConfig:
    email: str
    password: str


@dataclass
class DatabaseConfig:
    host: str = None
    port: int = None
    user: str = None
    password: str = None
    database: str = None


@dataclass
class VkApiConfig:
    token: str
    group_id: int


@dataclass
class Config:
    admin: AdminConfig
    session: SessionConfig = None
    database: DatabaseConfig = None
    vk_api: VkApiConfig = None


def setup_config(app: "Application", config_path: str):
    with open(config_path, "r") as f:
        raw_config = yaml.safe_load(f)

    app.config = Config(
        session=SessionConfig(
            key=raw_config["session"]["key"],
        ),
        admin=AdminConfig(
            email=raw_config["admin"]["email"],
            password=raw_config["admin"]["password"],
        ),
        database=DatabaseConfig(**raw_config["database"]),
        vk_api=VkApiConfig(
            token=raw_config["vk_api"]["token"],
            group_id=raw_config["vk_api"]["group_id"]
        ),
    )