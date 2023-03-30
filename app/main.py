"""
This file serves as the entry point for the application. 
It initializes the FastAPI app and imports the API routers.
"""
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

# Auth Imports
# -----------------
import secure
from app.auth.config import settings
from app.auth.dependencies import validate_token
from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
# -----------------

from app.internal.db import initialize_db
from app.domain.users import UsersDomain
from app.repository.users import UsersRepository
from app.routers.users import UsersRouter

# app = FastAPI()
app = FastAPI(openapi_url=None)

# Auth Config
# -----------------
csp = secure.ContentSecurityPolicy().default_src("'self'").frame_ancestors("'none'")
hsts = secure.StrictTransportSecurity().max_age(31536000).include_subdomains()
referrer = secure.ReferrerPolicy().no_referrer()
cache_value = secure.CacheControl().no_cache().no_store().max_age(0).must_revalidate()
x_frame_options = secure.XFrameOptions().deny()

secure_headers = secure.Secure(
    csp=csp,
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


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # settings.client_origin_url
    allow_methods=["*"], # "GET"
    allow_headers=["Authorization", "Content-Type"],
    allow_credentials=True,
    max_age=86400,
)
# -----------------

# # Configure CORS middleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

db = initialize_db()
users_repository = UsersRepository(db)
users_domain = UsersDomain(users_repository)
users_router = UsersRouter(users_domain)

app.include_router(users_router.router)

@app.get('/')
def index():
    return 'Hello from the MASLOW API'

# Auth Routes
# -----------------

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

# -----------------

# if __name__ == '__main__':
#     uvicorn.run("app.main:app", host="0.0.0.0", port=5000, log_level="info", reload=True)

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.port,
        log_level="info",
        reload=True,
        server_header=False,
    )

handler = Mangum(app)