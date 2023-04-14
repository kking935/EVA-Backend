from typing import List
from fastapi import APIRouter
from pydantic import BaseModel
from app.domain.surveys import SurveysDomain
from app.models import AnswerModel, QuestionsModel, ReportsModel, SurveyModel
from fastapi import APIRouter
from app.routers.base_router import create_base_router

def create_survey_router(domain: SurveysDomain):
    base_router = create_base_router(domain=domain, item_name='surveys', model=SurveyModel)

    @base_router.post('/new-survey', response_model=SurveyModel)
    def new_survey():
        return domain.new_survey()

    @base_router.put('/add-answer') # TODO: FIX THIS-> , response_model=QuestionsModel | ReportsModel)
    def add_answer(answer: AnswerModel):
        return domain.add_answer(answer)
    
    return base_router