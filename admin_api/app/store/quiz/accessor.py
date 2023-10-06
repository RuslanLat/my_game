# admin_api/app/store/quiz/accessor.py

from typing import Optional
from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload

from app.base.base_accessor import BaseAccessor
from app.quiz.models import (
    Question,
    Theme,
    ThemeModel,
    QuestionModel
)


class QuizAccessor(BaseAccessor):

    async def create_theme(self, title: str, lap: int) -> Theme:
        
        new_theme = ThemeModel(title=title, lap=lap)

        async with self.app.database.session.begin() as session:
            
            session.add(new_theme)

        return Theme(id=new_theme.id, title=new_theme.title, lap=lap)

    async def get_theme_by_title(self, title: str) -> Optional[Theme]:
        
        query = select(ThemeModel).where(ThemeModel.title == title)

        async with self.app.database.session() as session:
            
            theme: Optional[ThemeModel] = await session.scalar(query)
        
        if not theme:
            return None
        
        return Theme(id=theme.id, title=theme.title, lap=theme.lap)


    async def get_theme_by_id(self, id_: int) -> Optional[Theme]:
        
        query = select(ThemeModel).where(ThemeModel.id == id_)

        async with self.app.database.session() as session:
            
            theme: Optional[ThemeModel] = await session.scalar(query)
        

        if not theme:
            return None
        
        return Theme(id=theme.id, title=theme.title, lap=theme.lap)


    async def list_themes(self, lap: Optional[int] = None) -> list[Optional[Theme]]:

        query = select(ThemeModel)

        if lap:
            query = query.where(ThemeModel.lap == int(lap))

        async with self.app.database.session() as session:
            
            themes = await session.scalars(query)
        
        if not themes:
            return []
        
        return [Theme(id=theme.id, title=theme.title, lap=theme.lap) for theme in themes.all()]


    async def create_question(
            self, title: str, theme_id: int, answers: str, points: int,
            image_href: Optional[str] = None, audio_href: Optional[str] = None, media_id: Optional[int] = None) -> Question:

        new_question = QuestionModel(
            title=title,
            theme_id=theme_id,
            answers=answers,
            points=points,
            image_href=image_href,
            audio_href=audio_href,
            media_id=media_id
            )

        async with self.app.database.session.begin() as session:
            session.add(new_question)


        return Question(
            id=new_question.id,
            title=new_question.title,
            theme_id=new_question.theme_id,
            answers=new_question.answers,
            points=new_question.points,
            image_href=new_question.image_href,
            audio_href=new_question.audio_href,
            media_id=new_question.media_id,
        )


    async def get_question_by_title(self, title: str) -> Optional[Question]:

        query = (select(QuestionModel)
                .where(QuestionModel.title == title))

        async with self.app.database.session() as session:
            
            question: Optional[QuestionModel] = await session.scalar(query)
        
        if not question:
            return None

        return Question(
            id=question.id,
            title=question.title,
            theme_id=question.theme_id,
            answers=question.answers
        )

    async def list_questions(self, theme_id: Optional[int] = None) -> list[Question]:

        query = select(QuestionModel)

        if theme_id:
            query = query.where(QuestionModel.theme_id == int(theme_id))

        async with self.app.database.session() as session:
            
            questions = await session.scalars(query)
        


        return [
            Question(id=question.id,
                     title=question.title,
                     theme_id=question.theme_id,
                     answers=question.answers,
                     points=question.points,
                     image_href=question.image_href,
                     audio_href=question.audio_href,
                     media_id=question.media_id)
                for question in questions.unique()]