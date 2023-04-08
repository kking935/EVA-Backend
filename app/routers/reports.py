"""
This file handles the Report API endpoints (such as CRUD operations).
It passes request data to the domain layer and returns the response.
"""
from typing import List
from fastapi import APIRouter, HTTPException
from ..domain.reports import ReportsDomain, ReportsModel, EntryModel

class ReportsRouter:
    def __init__(self, reports_domain: ReportsDomain) -> None:
        self.__reports_domain = reports_domain

    @property
    def router(self):
        api_router = APIRouter(prefix='/reports', tags=['reports'])
        
        @api_router.get('/')
        def index_route():
            return 'EVA API Reports Route'
        
        @api_router.get('/all')
        def get_all():
            return self.__reports_domain.get_all()    

        @api_router.get('/{rid}')
        def get_report(rid: str):
            try:
                return self.__reports_domain.get_report(rid)
            except KeyError:
                raise HTTPException(status_code=400, detail='No report found')

        @api_router.post('/create')
        def create_report(form: List[EntryModel]):
            try:
                rid = self.__reports_domain.create_report(form)
                return rid
            except KeyError:
                raise HTTPException(status_code=400, detail='No report found')

        @api_router.delete('/delete/{rid}')
        def delete_report(rid: str):
            return self.__reports_domain.delete_report(rid)    
        
        return api_router