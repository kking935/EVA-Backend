'''
This file serves as a middleman between the router layer and the repository layer.
It receives requests from the router layer, handles the corresponding business logic,
and sends requests to the repository layer based on data that needs to be stored or 
retrieved from the database.
'''
from uuid import uuid4
from pydantic import Field, BaseModel
from typing import List, Optional, Dict

from ..repository.questions import QuestionsRepository

class QuestionsModel(BaseModel):
    qid: Optional[str] = None
    question: str = Field(..., example='What is your current living situation?')
    domains: Optional[List[str]] = Field(..., example=['Housing', 'Employment'])

class QuestionsDomain():
    def __init__(self, repository: QuestionsRepository) -> None:
        self.__repository = repository

    def get_all(self):
        return self.__repository.get_all()

    def get_question(self, qid: str):
        return self.__repository.get_question(qid)

    def create_question(self, question: QuestionsModel):
        question.qid = str(uuid4())
        return self.__repository.create_question(question.dict())
    
    def delete_question(self, qid: str):
        return self.__repository.delete_question(qid)