from uuid import uuid4
from pydantic import Field, BaseModel
from typing import List, Optional, Dict

from ..utils.gpt import build_report
from ..repository.users import UsersRepository

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
        report: ReportsModel = build_report(form, rid)
        response = self.__repository.create_report(user_uid, report)
        return rid

    def update_user(self, user: UsersModel):
        return self.__repository.update_user(user.dict())

    def delete_user(self, uid: str):
        return self.__repository.delete_user(uid)