# admin_api/app/quiz/views.py

from aiohttp_apispec import docs, request_schema, response_schema
from aiohttp.web_exceptions import HTTPConflict, HTTPNotFound, HTTPBadRequest
from sqlalchemy import exc

from app.quiz.schemes import (
    ThemeRequestSchema,
    ThemeListResponseSchema,
    ThemeListRequestQuerySchema,
    ThemeResponseSchema,
    QuestionRequestSchema,
    QuestionResponseSchema,
    QuestionListResponseSchema,
    QuestionListRequestQuerySchema,
)
from app.web.app import View
from app.web.mixins import AuthRequiredMixin
from app.web.utils import json_response


class ThemeAddView(AuthRequiredMixin, View):
    @request_schema(ThemeRequestSchema)
    @response_schema(ThemeResponseSchema)
    @docs(tags=["theme"], summary="Add theme view", description="Add theme to database")
    async def post(self):

        title = self.data["title"]
        lap = self.data["lap"]

        try:
            theme = await self.store.quizzes.create_theme(title=title, lap=lap)
        except exc.IntegrityError as e:
             if "23505" in e.orig.pgcode:
                raise HTTPConflict

        return json_response(data=ThemeResponseSchema().dump(theme))


class ThemeListView(AuthRequiredMixin, View):
    @request_schema(ThemeListRequestQuerySchema)
    @response_schema(ThemeListResponseSchema)
    @docs(tags=["theme"], summary="Add theme list view", description="Get themes list from database")
    async def get(self):
        lap = self.request.query.get("lap")
        themes = await self.store.quizzes.list_themes(lap)
        return json_response(ThemeListResponseSchema().dump({"themes" : themes}))


class QuestionAddView(AuthRequiredMixin, View):
    @request_schema(QuestionRequestSchema)
    @response_schema(QuestionResponseSchema)
    @docs(tags=["questions"], summary="Add question view", description="Add question to database")
    async def post(self):

        title = self.data["title"]
        theme_id = self.data["theme_id"]
        answers = self.data["answers"]
        points = self.data["points"]
        image_href = self.data["image_href"]
        audio_href = self.data["audio_href"]
        media_id = self.data["media_id"]
        
        try:
            question = await self.store.quizzes.create_question(
                title=title,
                theme_id=theme_id,
                answers=answers,
                points=points,
                image_href=image_href,
                audio_href=audio_href,
                media_id=media_id
            )

        except exc.IntegrityError as e:
            if "23503" in e.orig.pgcode:
                raise HTTPNotFound
        
        return json_response(QuestionResponseSchema().dump(question))
    

class QuestionListView(AuthRequiredMixin, View):
    @request_schema(QuestionListRequestQuerySchema)
    @response_schema(QuestionListResponseSchema)
    @docs(tags=["questions"], summary="Add questions list view", description="Get questions list from database")
    async def get(self):
        theme_id = self.request.query.get('theme_id')
        questions = await self.store.quizzes.list_questions(theme_id)
        return json_response(QuestionListResponseSchema().dump({"questions" : questions}))