import os
from mangum import Mangum
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import secure

from app.internal.db import initialize_db
from app.domain.users import UsersDomain
from app.repository.users import UsersRepository
from app.routers.users import UsersRouter
from app.domain.reports import ReportsDomain
from app.repository.reports import ReportsRepository
from app.routers.reports import ReportsRouter
from app.domain.questions import QuestionsDomain
from app.repository.questions import QuestionsRepository
from app.routers.questions import QuestionsRouter

import os
from dotenv import load_dotenv

load_dotenv()
stage = os.environ.get("STAGE", None)
port = int(os.environ.get("PORT", 5000))

root_path = f"/{stage}" if stage else "/"

app = FastAPI(title="EVA API", root_path=root_path)
csp = secure.ContentSecurityPolicy().default_src("'self'").frame_ancestors("'none'")
hsts = secure.StrictTransportSecurity().max_age(31536000).include_subdomains()
referrer = secure.ReferrerPolicy().no_referrer()
cache_value = secure.CacheControl().no_cache().no_store().max_age(0).must_revalidate()
x_frame_options = secure.XFrameOptions().deny()
secure_headers = secure.Secure(
    # csp=csp,
    hsts=hsts,
    referrer=referrer,
    cache=cache_value,
    xfo=x_frame_options,
)
    
@app.middleware("http")
async def set_secure_headers(request, call_next):
    response = await call_next(request)
    secure_headers.framework.fastapi(response)
    return response

origins = [
    "http://localhost",
    "http://localhost/",
    "https://localhost",
    "https://localhost/",
    "http://localhost:3000",
    "http://localhost:3000/",
    "https://localhost:3000",
    "https://localhost:3000/",
    "http://eva-ai.vercel.app",
    "http://eva-ai.vercel.app/",
    "https://eva-ai.vercel.app",
    "https://eva-ai.vercel.app/",
    "https://eva-ai.vercel.app/survey",
    "https://eva-ai.vercel.app/report"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

db = initialize_db()
users_repository = UsersRepository(db)
users_domain = UsersDomain(users_repository)
users_router = UsersRouter(users_domain)
app.include_router(users_router.router)

reports_repository = ReportsRepository(db)
reports_domain = ReportsDomain(reports_repository)
reports_router = ReportsRouter(reports_domain)
app.include_router(reports_router.router)

questions_repository = QuestionsRepository(db)
questions_domain = QuestionsDomain(questions_repository)
questions_router = QuestionsRouter(questions_domain)
app.include_router(questions_router.router)

@app.get('/')
def index():
    return 'EVA Root API'

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    message = str(exc.detail)
    return JSONResponse({"message": message}, status_code=exc.status_code)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        log_level="info",
        reload=True,
    )

handler = Mangum(app)