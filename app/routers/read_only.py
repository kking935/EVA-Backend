"""
This file handles the Report API endpoints (such as CRUD operations).
It passes request data to the domain layer and returns the response.
"""
from typing import List
from pydantic import BaseModel
from fastapi import APIRouter

from app.domain.base_domain import BaseDomain
from app.routers.base_router import create_base_router

def create_read_only_router(domain: BaseDomain, model: BaseModel, item_name: str):
    read_only_router = APIRouter()
    base_router = create_base_router(domain=domain, item_name=item_name, model=model)

    for route in base_router.routes:
        if route.name == 'get_all' or route.name == 'get':
            read_only_router.routes.append(route)

    return read_only_router