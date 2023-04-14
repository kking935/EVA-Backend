from pydantic import Field, BaseModel
from typing import Dict, List, Optional

class SublabelModel(BaseModel):
    slid: str = Field(..., example='11')
    sublabel: str = Field(..., example='Poverty')

class LabelsModel(BaseModel):
    lid: str = None
    label: str = Field(..., example='Economic Stability')
    sublabels: List[SublabelModel] = Field(..., example=[SublabelModel(slid='11', sublabel='Poverty')])

class QuestionsModel(BaseModel):
    qid: Optional[str] = None
    question: str = Field(..., example='What is your current living situation?')
    labels: Optional[List[LabelsModel]] = None

class EntryModel(BaseModel):
    qid: str = Field(..., example='1')
    question: str = Field(..., example='What is your current living situation?')
    answer: str = Field(..., example='I am currently homeless')

class AnswerModel(BaseModel):
    sid: str = Field(..., example='1')
    qid: str = Field(..., example='1')
    question: str = Field(..., example='What is your current living situation?')
    answer: str = Field(..., example='I am homeless')

class SurveyQuestion(BaseModel):
    qid: str = Field(..., example='1')
    question: str = Field(..., example='What is your current living situation?')
    answer: Optional[str] = None
    risk_factors: Optional[Dict] = None

class SurveyModel(BaseModel):
    sid: Optional[str] = None
    survey: Optional[Dict[str, SurveyQuestion]] = None
    cur_qid: Optional[str] = '1'

class Message(BaseModel):
    role: str
    content: str

class ReportsModel(BaseModel):
    rid: Optional[str] = None
    survey: Dict[str, SurveyQuestion]
    messages: Optional[List[Message]] = None
    overall_risk_factor: Optional[Dict[str, List[str]]] = Field(..., example={'risk_factor': 'high', 'risk_level': 'high'})
    summary: Optional[str] = Field(..., example='Report summary')

class UsersModel(BaseModel):
    uid: Optional[str] = None
    fname: str = Field(..., example='Ken')
    lname: str = Field(..., example='King')
    rids: Optional[List[str]] = None
    sids: Optional[List[str]] = None