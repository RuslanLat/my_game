from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime

from app.store.database.sqlalchemy_base import db


@dataclass
class Player:

    vk_id: int
    first_name: str
    last_name: str


@dataclass
class PlayerLeaderBoard:
    first_name: str
    last_name: str
    points: str


@dataclass
class Game:
    id: int
    created_at: datetime
    peer_id: int
    status: bool


@dataclass
class GameSession:
    id: int
    game_id: int
    player_id: int
    points: int


@dataclass
class Points:
    points: int


class PlayerModel(db):

    __tablename__ = "players"

    vk_id = Column(Integer, primary_key=True)
    name = Column(String)
    last_name = Column(String)
    game_sessions = relationship("GameSessionModel")


class GameModel(db):

    __tablename__ = "games"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    peer_id = Column(Integer)
    status = Column(Boolean)
    game_sessions = relationship("GameSessionModel")


class GameSessionModel(db):

    __tablename__ = "game_sessions"

    id = Column(Integer, primary_key=True)
    # relationship: players
    game_id = Column(ForeignKey("games.id" , ondelete="CASCADE"), nullable=False)
    # relationship: players
    player_id = Column(ForeignKey("players.vk_id" , ondelete="CASCADE"), nullable=False)
    points = Column(Integer)