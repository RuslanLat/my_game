from typing import Optional, List
from sqlalchemy import select, update, and_
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.orm import aliased
from sqlalchemy import func 
from app.base.base_accessor import BaseAccessor
from app.games.models import (
    GameModel,
    Game,
    PlayerModel,
    Player,
    GameSessionModel,
    GameSession,
    PlayerLeaderBoard,
    Points
)
from app.store.vk_api.dataclasses import Members


class GameAccessor(BaseAccessor):

    async def create_players(self, players: List[Members]) -> List[Player]:
        
        new_players = [PlayerModel(vk_id=player.vk_id,
                                   name=player.first_name,
                                   last_name=player.last_name)
                      for player in players]

        async with self.app.database.session.begin() as session:
            
            session.add_all(new_players)

        return [Player(vk_id=player.vk_id,
                       first_name=player.name,
                       last_name=player.last_name)
               for player in new_players]
    

    async def create_player(self, player: Members) -> Player:
        
        new_player = PlayerModel(vk_id=player.vk_id,
                                   name=player.first_name,
                                   last_name=player.last_name)

        async with self.app.database.session.begin() as session:
            
            session.add(new_player)

        return Player(vk_id=new_player.vk_id,
                       first_name=new_player.name,
                       last_name=new_player.last_name)
    

    async def get_player_by_id(self, vk_id: int) -> Optional[Player]:
        
        query = select(PlayerModel).where(PlayerModel.vk_id == vk_id)

        async with self.app.database.session() as session:
            
            player: Optional[PlayerModel] = await session.scalar(query)
        

        if not player:
            return None
        
        return Player(vk_id=player.vk_id, first_name=player.name, last_name=player.last_name)
    

    async def create_game(self, peer_id: int) -> Game:
        
        game = GameModel(peer_id=peer_id, status=True)

        async with self.app.database.session.begin() as session:
            
            session.add(game)

        return Game(game.id, game.created_at, game.peer_id, game.status)
    

    async def create_game_session(self, game_id: int, players: List[Player]) -> GameSession:
        
        game_session = [GameSessionModel(game_id=game_id,
                                        player_id=player.vk_id,
                                        points=0)
                        for player in players]

        async with self.app.database.session.begin() as session:
            
            session.add_all(game_session)
        
        return [GameSession(id=game_ses.id,
                            game_id=game_ses.game_id,
                            player_id=game_ses.player_id,
                            points=game_ses.points) for game_ses in game_session]
    


    async def update_status_game(self, game_id: int) -> Optional[Game]:
        
        query = update(GameModel).where(and_(
            GameModel.peer_id == game_id,
            GameModel.status)).values(status=False)

        async with self.app.database.session.begin() as session:
            
            await session.execute(query)
        
        return None
    

    
    async def get_leader_board(self, game_id: int) -> Optional[PlayerLeaderBoard]:
        
        # query = (select(GameModel).where(and_(
        #     GameModel.peer_id == game_id,
        #     GameModel.created_at == select(func.max(GameModel.created_at))))
        #                  .options(joinedload(GameModel.game_sessions))
        #         )
        # #  .options(joinedload(GameModel.game_sessions))

        # async with self.app.database.session() as session:
            
        #     game_session = await session.scalars(query)

        # points_list = []
        # vk_ids = []
        # for player in game_session.unique():
        #     for p in player.game_sessions:
        #         points_list.append(Points(points=p.points))
        #         vk_ids.append(p.player_id)

        # query = (select(PlayerModel).filter(PlayerModel.vk_id.in_(vk_ids)))

        # async with self.app.database.session() as session:
            
        #     game_session = await session.scalars(query)

        # return [PlayerLeaderBoard(first_name=player.name,
        #                           last_name=player.last_name,
        #                           points=str(points_list[vk_ids.index(player.vk_id)].points))
        #                           for player in game_session.unique()]

        query = (select(GameModel).where(
            GameModel.peer_id == game_id).order_by(GameModel.id.desc()).limit(1)
            .options(joinedload(GameModel.game_sessions)))
                
        #  .options(joinedload(GameModel.game_sessions))

        async with self.app.database.session() as session:
            
            game_session = await session.scalars(query)

        points_list = []
        vk_ids = []
        for player in game_session.unique():
            for p in player.game_sessions:
                points_list.append(Points(points=p.points))
                vk_ids.append(p.player_id)

        query = (select(PlayerModel).filter(PlayerModel.vk_id.in_(vk_ids)))

        async with self.app.database.session() as session:
            
            game_session = await session.scalars(query)

        return [PlayerLeaderBoard(first_name=player.name,
                                  last_name=player.last_name,
                                  points=str(points_list[vk_ids.index(player.vk_id)].points))
                                  for player in game_session.unique()]
    

    async def update_points(self, peer_id: int, vk_id: int, points: int):


        query = select(GameModel).where(GameModel.peer_id == peer_id).order_by(GameModel.id.desc()).limit(1)

        async with self.app.database.session() as session:
            
            game = await session.scalar(query)

        id_game = game.id

        query = update(GameSessionModel).where(and_(
            GameSessionModel.game_id == id_game,
            GameSessionModel.player_id == vk_id)).values(points=GameSessionModel.points + points)

        async with self.app.database.session.begin() as session:
            
            await session.execute(query)
        
        return None
    

    async def random_player(self, game_id: int) -> List[Player]:
        
        query = (select(GameModel).where(and_(
            GameModel.peer_id == game_id,
            GameModel.created_at == select(func.max(GameModel.created_at))))
                         .options(joinedload(GameModel.game_sessions))
                )
        #  .options(joinedload(GameModel.game_sessions))

        async with self.app.database.session() as session:
            
            game_session = await session.scalars(query)

        vk_ids = []
        for player in game_session.unique():
            for p in player.game_sessions:
                vk_ids.append(p.player_id)

        query = (select(PlayerModel).filter(PlayerModel.vk_id.in_(vk_ids)))

        async with self.app.database.session() as session:
            
            game_session = await session.scalars(query)

        return [Player(vk_id=player.vk_id,
                       first_name=player.name,
                       last_name=player.last_name)
                       for player in game_session.unique()]
