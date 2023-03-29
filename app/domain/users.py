"""
This file defines the user-related models and business rules that are used throughout the application.
It defines the properties and methods of a user object, as well as the rules and constraints that apply to user data.
It is used by the API routers and repository layer to ensure that user data is stored and retrieved correctly.
"""

from uuid import uuid4
from app.helpers.form import build_survey
from app.helpers.gpt import build_report
from pydantic import Field
from pydantic import BaseModel
# from pydantic.types import UUID4
from typing import List, Optional, Dict

from app.repository.users import UsersRepository

class EntryModel(BaseModel):
    question_id: str = Field(..., example='1')
    question: str = Field(..., example='What is your name?')
    answer: str = Field(..., example='Ken')

class ReportsModel(BaseModel):
    rid: Optional[str] = None
    survey: Dict[str, Dict] = Field(..., example={'question1': {'answer': 'answer1'}})
    overall_risk_factor: Optional[Dict[str, Dict]] = Field(..., example={'risk_factor': 'high', 'risk_level': 'high'})
    summary: Optional[str] = Field(..., example='Report summary')

class UsersModel(BaseModel):
    uid: Optional[str] = None
    fname: str = Field(..., example='Ken')
    lname: str = Field(..., example='King')
    reports: Optional[Dict[str, ReportsModel]] = {}

class UsersDomain():
    def __init__(self, repository: UsersRepository) -> None:
        self.__repository = repository

    def get_all(self):
        return self.__repository.get_all()

    def get_user(self, uid: str):
        return self.__repository.get_user(uid)

    def get_report(self, user_uid: str, report_uid: str):
        return self.__repository.get_report(user_uid, report_uid)
    
    def create_user(self, user: UsersModel):
        user.uid = str(uuid4())
        return self.__repository.create_user(user.dict())
    
    def create_report(self, user_uid: str, form: List[EntryModel]):
        rid = str(uuid4())
        report: ReportsModel = {
            "rid": rid,
            "summary": '',
            "survey": build_survey(form)
        }
        build_report(report)
        response = self.__repository.create_report(user_uid, report)
        return rid

    def update_user(self, user: UsersModel):
        return self.__repository.update_user(user.dict())

    def delete_user(self, uid: str):
        return self.__repository.delete_user(uid)