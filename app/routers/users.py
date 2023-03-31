"""
This file handles the User API endpoints (such as CRUD operations).
It passes request data to the domain layer and returns the response.
"""
from typing import List
from fastapi import APIRouter, HTTPException
from ..domain.users import UsersDomain, UsersModel, EntryModel

class UsersRouter:
    def __init__(self, users_domain: UsersDomain) -> None:
        self.__users_domain = users_domain

    @property
    def router(self):
        api_router = APIRouter(prefix='/users', tags=['users'])
        
        @api_router.get('/')
        def index_route():
            return 'EVA API Users Route'
        
        @api_router.get('/all')
        def get_all():
            return self.__users_domain.get_all()    

        @api_router.get('/{user_uid}')
        def get_user(user_uid: str):
            try:
                return self.__users_domain.get_user(user_uid)
            except KeyError:
                raise HTTPException(status_code=400, detail='No user found')

        @api_router.get('/{user_uid}/reports/{report_uid}')
        def get_report(user_uid: str, report_uid: str):
            try:
                return self.__users_domain.get_report(user_uid, report_uid)
            except KeyError:
                raise HTTPException(status_code=400, detail='No report found')

        @api_router.post('/create')
        def create_user(users_model: UsersModel):
            return self.__users_domain.create_user(users_model)
        
        @api_router.post('/{user_uid}/reports/create')
        def create_report(user_uid: str, form: List[EntryModel]):
            try:
                rid = self.__users_domain.create_report(user_uid, form)
                return rid
            except KeyError:
                raise HTTPException(status_code=400, detail='No user found')
            
        @api_router.put('/update')
        def update_user(users_model: UsersModel):
            return self.__users_domain.update_user(users_model)

        @api_router.delete('/delete/{user_uid}')
        def delete_user(user_uid: str):
            return self.__users_domain.delete_user(user_uid)

        return api_router