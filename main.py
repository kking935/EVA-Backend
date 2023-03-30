import os
from mangum import Mangum
import uvicorn
from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
import secure

from app.auth.config import settings
from app.auth.dependencies import validate_token
from app.internal.db import initialize_db
from app.domain.users import UsersDomain
from app.repository.users import UsersRepository
from app.routers.users import UsersRouter

stage = os.environ.get('STAGE', None)
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

@app.get('/')
def index():
    return 'Hello from the MASLOW API'

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    message = str(exc.detail)
    return JSONResponse({"message": message}, status_code=exc.status_code)

@app.get("/api/messages/public")
def public():
    return {"text": "This is a public message."}

@app.get("/api/messages/protected", dependencies=[Depends(validate_token)])
def protected(request: Request):
    print(request.state.payload)
    return {"text": f"This is a protected message, your user id is {request.state.payload['sub']}"}

@app.get("/api/messages/admin", dependencies=[Depends(validate_token)])
def admin():
    return {"text": "This is an admin message."}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.port,
        log_level="info",
        reload=True,
        server_header=False,
    )

handler = Mangum(app)