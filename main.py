from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from settings.settings import HOMERO_BUCKET_NAME, PETTER_GRIFFIN_BUCKET_NAME

from blueprints.index.index import index_router
from blueprints.minio.minio_blueprint import minio_router
from services.minio_service import MinioService
from errors.api_error import ApiError
from utils.utils import create_buckets_from_config

minio_service = MinioService()
create_buckets_from_config()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)
app.include_router(index_router)
app.include_router(minio_router)

@app.exception_handler(ApiError)
async def api_error_handler(request: Request, exception: ApiError):
    return JSONResponse(
        status_code=exception.status_code,
        content={
            "message": exception.message,
            "description": exception.description,
        },
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": f"Error inesperado: {str(exc)}"},
    )
