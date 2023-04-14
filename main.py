import os
from mangum import Mangum
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import secure
from app.internal.db import initialize_db
from app.routers.setup_routes import setup_routes
from app.config.server_settings import MIDDLEWARE_SETTINGS, SECURITY_SETTINGS
import os
from dotenv import load_dotenv
load_dotenv()

app = FastAPI(title="EVA API", root_path="/")

app.add_middleware(CORSMiddleware, **MIDDLEWARE_SETTINGS)
# secure_headers = secure.Secure(**SECURITY_SETTINGS)
# @app.middleware("http")
# async def set_secure_headers(request, call_next):
#     response = await call_next(request)
#     secure_headers.framework.fastapi(response)
#     return response

db = initialize_db()
setup_routes(app, db)

# @app.get('/')
# def index():
#     return 'EVA Root API'

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    message = str(exc.detail)
    return JSONResponse({"message": message}, status_code=exc.status_code)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        log_level="info",
        reload=True,
    )

handler = Mangum(app)