'''
This file serves as a middleman between the router layer and the repository layer.
It receives requests from the router layer, handles the corresponding business logic,
and sends requests to the repository layer based on data that needs to be stored or 
retrieved from the database.
'''
from uuid import uuid4
from pydantic import Field, BaseModel
from typing import List, Optional, Dict

from app.domain.reports import ReportsModel
from ..repository.users import UsersRepository

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

    def create_user(self, user: UsersModel):
        user.uid = str(uuid4())
        return self.__repository.create_user(user.dict())
    
    def delete_user(self, uid: str):
        return self.__repository.delete_user(uid)