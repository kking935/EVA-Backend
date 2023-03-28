"""
This file serves as the entry point for the application. 
It initializes the FastAPI app and imports the API routers.
"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.internal.db import initialize_db
from app.domain.users import UsersDomain
from app.repository.users import UsersRepository
from app.routers.users import UsersRouter

app = FastAPI()

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = initialize_db()
users_repository = UsersRepository(db)
users_domain = UsersDomain(users_repository)
users_router = UsersRouter(users_domain)

app.include_router(users_router.router)

@app.get('/')
def index():
    return 'Hello from the MASLOW API'

if __name__ == '__main__':
    uvicorn.run("app.main:app", host="0.0.0.0", port=5000, log_level="info", reload=True)