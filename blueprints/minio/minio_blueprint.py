from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from fastapi import status
from services.minio_service import MinioService
from minio import S3Error

minio_router = APIRouter()
minio_service = MinioService()

@minio_router.get("/imagenes/{personaje}")

async def get_objects_from_bucket(personaje:str):
    try:

        objects = minio_service.list_all_object_names(personaje)
    except S3Error as error:
        print("Error : ", error)
        


    return objects