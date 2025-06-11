import random
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from fastapi import status
from minio import S3Error

from errors.api_error import ApiError
from services.minio_service import MinioService
from utils.utils import translate_personaje_to_bucket_name

minio_router = APIRouter()
minio_service = MinioService()

@minio_router.get("/imagenes/{personaje}")

async def get_objects_from_bucket(personaje:str)-> list[dict[str,str]]:
    """Gets all objects from a bucket

    Args:
        personaje (str): The name of the desired character

    Raises:
        ApiError:

    Returns:
        str: A list with objects
    """
    try:
        bucket = translate_personaje_to_bucket_name(personaje)
        objects = minio_service.list_all_object_names(bucket)
    except S3Error as error:
        raise ApiError(message="Error inesperado en el bucket de Minio", status_code=500, description="Ocurrio un error interno en el bucket de minio") from error
    return objects

@minio_router.get("/random-image/{personaje}")

async def get_random_image_from_bucket(personaje:str):
    """Gets a random object from a bucket

    Args:
        personaje (str): The name of the desired character

    Raises:
        ApiError

    Returns:
        str: A random object
    """
    try:
        bucket = translate_personaje_to_bucket_name(personaje)
        objects = minio_service.list_all_object_names(bucket)
        random_object = random.choice(objects)
    except S3Error as error:
        raise ApiError(message="Error inesperado en el bucket de Minio", status_code=500, description="Ocurrio un error interno en el bucket de minio") from error
    return random_object