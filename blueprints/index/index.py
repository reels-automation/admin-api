import logging
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from fastapi import status
from services.minio_service import MinioService
from settings.settings import MODELOS_VOCES, BUCKETS_DATA

index_router = APIRouter()
minio_service = MinioService()

def get_items_by_extension(bucket:str, extension:str) -> list[str]:

    items_from_bucket = minio_service.list_all_object_names(bucket)
    filtered_items = []
    for item in items_from_bucket:
        object_name = item["object_name"]
        split_object = object_name.split(".")
        if split_object[1] == extension:
            filtered_items.append(split_object[0])
    return filtered_items

@index_router.get("/")
async def personajes():

    voice_models_bucket = BUCKETS_DATA["voice-model"]
    personajes_images_bucket = BUCKETS_DATA["personajes-imagenes"]

    personajes_disponibles = []
    personajes_pth = get_items_by_extension(voice_models_bucket, "pth")
    personajes_index = get_items_by_extension(voice_models_bucket, "index")
    personajes_images = get_items_by_extension(personajes_images_bucket, "png")

    # En base a la lista de PTHs verificar si:
    #1) Existe su .index
    #2) Existe ALGUNA imágen 

    for personaje_pth in personajes_pth:
        logging.info(f"Analizando pth de:{personaje_pth}")
        if personaje_pth not in personajes_index:
            logging.info(f"No existe el .index de: {personaje_pth}")
            continue          
        personaje , lang = personaje_pth.rsplit("_",1) #Divide el guion de derecha a izquierda y solo el último. Le saca el _es , _en
        for personaje_image in personajes_images:
            image_name , number = personaje_image.rsplit("_",1)
            if image_name == personaje:
                personajes_disponibles.append(personaje_pth)
                break

    return personajes_disponibles

