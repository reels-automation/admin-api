import random
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from fastapi import status
from minio import S3Error

from errors.api_error import ApiError
from services.minio_service import MinioService
from utils.utils import translate_personaje_to_bucket_name
from settings.settings import VOICE_MODEL_BUCKET

minio_router = APIRouter()
minio_service = MinioService()

@minio_router.get("/imagenes/{personaje}")

async def get_images_from_personaje_name(personaje:str)-> list[dict[str,str]]:
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

async def get_random_image_from_personaje_name(personaje:str):
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

@minio_router.get("/get-file/{bucket}/{filename}")
async def get_file_from_bucket(bucket:str, filename:str):    
    try:
        objects = minio_service.list_all_object_names(bucket)
        for object in objects:
            if object['object_name'] != filename:
                continue
            else:
                return object['object_url']
    except S3Error as error:
        raise ApiError(message="Error inesperado en el bucket de Minio", status_code=500, description="Ocurrio un error interno en el bucket de minio") from error
    except Exception as error:
        raise ApiError(message="Error Interno", status_code=500, description="Ocurrio un error interno en el servidor") from error
    raise ApiError(message="Archivo no encontrado", status_code=404, description=f"El archivo: {filename} no existe en el bucket: {bucket}")

@minio_router.get("/get-voice-model-pth/{personaje}/{idioma}")
async def get_voice_model_pth_from_name(personaje:str, idioma:str):
    search_name_voice_model = f"{personaje}_{idioma}.pth"  
    
    try:
        objects = minio_service.list_all_object_names(VOICE_MODEL_BUCKET)
        for object in objects:
            if object['object_name'] != search_name_voice_model:
                continue
            else:
                response = {"name": object["object_name"], "url": object["object_url"]}
                return response
    except S3Error as error:
        print("ERROR: ", error)
        raise ApiError(message="Error inesperado en el bucket de Minio", status_code=500, description="Ocurrio un error interno en el bucket de minio") from error
    except Exception as error:
        raise ApiError(message="Error Interno", status_code=500, description="Ocurrio un error interno en el servidor") from error
    raise ApiError(message="Archivo no encontrado", status_code=404, description=f"El archivo: {search_name_voice_model} no existe en el bucket: {VOICE_MODEL_BUCKET}")

@minio_router.get("/get-voice-model-index/{personaje}/{idioma}")
async def get_voice_model_index_from_name(personaje:str, idioma:str):
    search_name_voice_model = f"{personaje}_{idioma}.index"
    try:
        objects = minio_service.list_all_object_names(VOICE_MODEL_BUCKET)
        for object in objects:
            if object['object_name'] != search_name_voice_model:
                continue
            else:
                response = {"name": object["object_name"], "url": object["object_url"]}
                return response
    except S3Error as error:
        raise ApiError(message="Error inesperado en el bucket de Minio", status_code=500, description="Ocurrio un error interno en el bucket de minio") from error
    except Exception as error:
        raise ApiError(message="Error Interno", status_code=500, description="Ocurrio un error interno en el servidor") from error
    raise ApiError(message="Archivo no encontrado", status_code=404, description=f"El archivo: {search_name_voice_model} no existe en el bucket: {VOICE_MODEL_BUCKET}")

@minio_router.get("/get-files/{bucket}")
async def get_all_file_from_bucket(bucket:str):    
    try:
        objects = minio_service.list_all_object_names(bucket)
    except S3Error as error:
        raise ApiError(message="Error inesperado en el bucket de Minio", status_code=500, description="Ocurrio un error interno en el bucket de minio") from error
    return objects