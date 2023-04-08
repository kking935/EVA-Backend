'''
This file serves as a middleman between the router layer and the repository layer.
It receives requests from the router layer, handles the corresponding business logic,
and sends requests to the repository layer based on data that needs to be stored or 
retrieved from the database.
'''
from uuid import uuid4
from pydantic import Field, BaseModel
from typing import List, Optional, Dict

from ..repository.reports import ReportsRepository
from ..utils.gpt_handler import build_report

class EntryModel(BaseModel):
    question_id: str = Field(..., example='1')
    question: str = Field(..., example='What is your current living situation?')
    answer: str = Field(..., example='I am currently homeless')

class ReportsModel(BaseModel):
    rid: Optional[str] = None
    survey: Dict[str, Dict] = Field(..., example={'question1': {'answer': 'answer1'}})
    overall_risk_factor: Optional[Dict[str, Dict]] = Field(..., example={'risk_factor': 'high', 'risk_level': 'high'})
    summary: Optional[str] = Field(..., example='Report summary')

class ReportsDomain():
    def __init__(self, repository: ReportsRepository) -> None:
        self.__repository = repository

    def get_all(self):
        return self.__repository.get_all()

    def get_report(self, rid: str):
        return self.__repository.get_report(rid)

    def create_report(self, form: List[EntryModel]):
        rid = str(uuid4())
        report: ReportsModel = build_report(form, rid)
        response = self.__repository.create_report(report)
        return rid
    
    def delete_report(self, rid: str):
        return self.__repository.delete_report(rid)