"""
This file handles the Report API endpoints (such as CRUD operations).
It passes request data to the domain layer and returns the response.
"""
from typing import List
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from app.domain.base_domain import BaseDomain

def create_base_router(
        domain: BaseDomain, 
        item_name: str, 
        model: BaseModel,
        create_request_model: BaseModel = None, 
    ):
    base_router = APIRouter(prefix=f"/{item_name}", tags=[item_name])

    @base_router.get('/all') # TODO: Fix this -> , response_model=List[model])
    def get_all():
        return domain.get_all()    

    @base_router.get('/{id}') # TODO: Fix this -> , response_model=model)
    def get(id: str):
        try:
            return domain.get(id)
        except KeyError:
            raise HTTPException(status_code=400, detail=f'No item found in {item_name} with id {id}')

    @base_router.post('/create', response_model=model)
    def create(item_model: model if not create_request_model else create_request_model):
        return domain.create(item_model)
    
    @base_router.put('/update', response_model=model)
    def update(item_model: model):
        return domain.update(item_model)

    @base_router.delete('/delete/{id}')
    def delete(id: str):
        return domain.delete(id)   

    return base_router