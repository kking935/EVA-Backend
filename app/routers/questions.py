"""
This file handles the Question API endpoints (such as CRUD operations).
It passes request data to the domain layer and returns the response.
"""
from typing import List
from fastapi import APIRouter, HTTPException
from ..domain.questions import QuestionsDomain, QuestionsModel

class QuestionsRouter:
    def __init__(self, questions_domain: QuestionsDomain) -> None:
        self.__questions_domain = questions_domain

    @property
    def router(self):
        api_router = APIRouter(prefix='/questions', tags=['questions'])
        
        @api_router.get('/')
        def index_route():
            return 'EVA API Questions Route'
        
        @api_router.get('/all')
        def get_all():
            return self.__questions_domain.get_all()    

        @api_router.get('/{qid}')
        def get_question(qid: str):
            try:
                return self.__questions_domain.get_question(qid)
            except KeyError:
                raise HTTPException(status_code=400, detail='No question found')

        @api_router.post('/create')
        def create_question(question: QuestionsModel):
            try:
                qid = self.__questions_domain.create_question(question)
                return qid
            except KeyError:
                raise HTTPException(status_code=400, detail='No question found')

        @api_router.delete('/delete/{qid}')
        def delete_question(qid: str):
            return self.__questions_domain.delete_question(qid)    
        
        return api_router